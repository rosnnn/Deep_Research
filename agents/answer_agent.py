from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

class AnswerAgent:
    def __init__(self, model_name="gpt2-medium"):
        print("[🧠] Loading local LLM model...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            self.device = torch.device("cpu")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map=None,
                torch_dtype=torch.float32
            ).to(self.device)
            print("[✅] Model loaded successfully!")
        except Exception as e:
            print(f"[❌] Failed to load model: {e}")
            raise

    def draft_answer(self, context, question):
        try:
            if len(context.split()) < 30:
                return "The provided context seems too short. Please provide more information for a better answer."

            prompt = (
                f"Context: {context[:1000]}\n\n"  # Truncate context if too long
                f"Question: {question}\n"
                "Provide a concise, direct answer (1-2 sentences). Only include the most relevant information. Avoid unnecessary elaboration."
            )
            
            max_length = 1024  
            inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=max_length)

            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            input_ids = inputs["input_ids"]
            attention_mask = inputs["attention_mask"]

            output = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=50,  
                temperature=0.7,    
                top_p=0.85,          
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id
            )

            answer = self.tokenizer.decode(output[0], skip_special_tokens=True)
            
            print(f"[DEBUG] Raw generated answer: {answer}")
            
            answer = re.sub(r"\[\d+\]", "", answer).strip()  
            answer = answer.split('.')[0] + '.'  
            
            if len(answer.split()) < 5:
                return "The answer is too short or unclear. Try refining your question or providing more context."

            return answer
        except Exception as e:
            print(f"[❌] Failed to generate answer: {e}")
            return "Error generating answer."
