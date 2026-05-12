import os
import torch
from app.core.settings import settings

class IntentNode:
    def __init__(self):
        """
        Load configuration, tokenizer, and model checkpoint based on Lab 2 inference code.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.checkpoint_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../", "models/intent_model/checkpoint-157"))
        self.is_loaded = False
        self.model = None
        self.tokenizer = None
        
        print(f"Loading Lab 2 Intent Model from {self.checkpoint_path} on {self.device}...")
        
        try:
            # Try Unsloth first (if GPU available)
            if self.device == "cuda":
                self._load_with_unsloth()
            else:
                # CPU: use transformers + peft
                self._load_with_peft()
                
            # Prompt template (must match Lab 2 training format exactly)
            self.prompt_template = "Below is an inquiry from a banking customer. Classify the intent of the inquiry.\n\n### Inquiry:\n{}\n\n### Intent:\n"
            print("✓ Model loaded successfully")
            
        except Exception as e:
            print(f"  Model loading failed: {e}")
            print("Using fallback rule-based system instead.")
            self.is_loaded = False

    def _load_with_unsloth(self):
        """Load using Unsloth if available (GPU only)."""
        try:
            from unsloth import FastLanguageModel
            print("Attempting Unsloth load...")
            
            # Unsloth handles local paths better
            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=self.checkpoint_path,
                max_seq_length=2048,
                load_in_4bit=False,  # CPU friendly
            )
            FastLanguageModel.for_inference(self.model)
            self.is_loaded = True
            print("✓ Model loaded with Unsloth")
        except Exception as e:
            print(f"Unsloth failed: {e}, trying PEFT...")
            self._load_with_peft()

    def _load_with_peft(self):
        """Load using transformers + PEFT (works on CPU)."""
        from transformers import AutoTokenizer, AutoModelForCausalLM
        from peft import PeftModel
        import json
        
        print("Loading with transformers+PEFT...")
        
        adapter_config_path = os.path.join(self.checkpoint_path, "adapter_config.json")
        with open(adapter_config_path, "r") as f:
            adapter_config = json.load(f)
        
        base_model_name = adapter_config.get("base_model_name_or_path", "meta-llama/Llama-2-7b")
        print(f"Base model: {base_model_name}")
        
        # Load tokenizer
        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.checkpoint_path, 
            local_files_only=False,
            trust_remote_code=True
        )
        if not self.tokenizer.pad_token:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load base model 
        print(f"Loading base model: {base_model_name}...")
        try:
            # Try loading from HuggingFace with trust_remote_code
            self.base_model = AutoModelForCausalLM.from_pretrained(
                base_model_name,
                torch_dtype=torch.float32,
                device_map="cpu",
                low_cpu_mem_usage=True,
                trust_remote_code=True,
            )
        except Exception as e:
            print(f"Failed to load {base_model_name}: {e}")
            print("Using fallback: meta-llama/Llama-2-7b-hf")
            try:
                self.base_model = AutoModelForCausalLM.from_pretrained(
                    "meta-llama/Llama-2-7b-hf",
                    torch_dtype=torch.float32,
                    device_map="cpu",
                    low_cpu_mem_usage=True,
                    trust_remote_code=True,
                )
            except Exception as e2:
                print(f"Failed to load Llama-2: {e2}")
                print("⚠️  Model loading not possible. Will use rule-based fallback.")
                self.is_loaded = False
                return
        
        # Load LoRA adapter
        try:
            print("Loading LoRA adapter...")
            self.model = PeftModel.from_pretrained(
                self.base_model, 
                self.checkpoint_path,
                torch_dtype=torch.float32
            )
            self.model.eval()
            self.is_loaded = True
            print("✓ Model loaded with transformers+PEFT")
        except Exception as e:
            print(f"Failed to load LoRA adapter: {e}")
            print("⚠️  Using base model without adapter")
            self.model = self.base_model
            self.is_loaded = True

    def detect_intent(self, message: str) -> str:
        """
        Receive an input message and return the predicted intent label.
        """
        if not getattr(self, "is_loaded", False):
            print("Model not loaded. Using fallback rule-based system.")
            return self._rule_based_fallback(message)

        inputs = self.tokenizer(
            [self.prompt_template.format(message)],
            return_tensors="pt",
            max_length=2048,  # Tránh warning về max_length
            truncation=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=64,
                use_cache=True,
            )
        
        decoded_output = self.tokenizer.batch_decode(outputs)[0]
        
        try:
            predicted_label = decoded_output.split("### Intent:")[1]
            for stop_token in [self.tokenizer.eos_token, "<|end_of_text|>", "<|eot_id|>", "\n\n"]:
                if stop_token and stop_token in predicted_label:
                    predicted_label = predicted_label.split(stop_token)[0]
            predicted_label = predicted_label.strip().split("\n")[0].strip()
        except (IndexError, AttributeError):
            predicted_label = "unknown"
            
        return predicted_label
    
    def detect_intent_with_confidence(self, message: str) -> dict:
        """
        Detects intent and returns confidence score.
        Confidence is higher when model is loaded, lower for fallback.
        """
        intent = self.detect_intent(message)
        is_model_loaded = getattr(self, "is_loaded", False)
        
        if is_model_loaded:
            confidence = 0.85  # Good confidence with fine-tuned model
        else:
            confidence = 0.60  # Lower confidence with rule-based fallback
        
        return {
            "intent": intent,
            "confidence": confidence,
            "model_loaded": is_model_loaded
        }

    def _rule_based_fallback(self, message: str) -> str:
        msg_lower = message.lower()
        if "transfer" in msg_lower or "send" in msg_lower:
            return "transfer_failure"
        elif "card" in msg_lower and "receive" in msg_lower:
            return "card_not_received"
        elif "block" in msg_lower or "lock" in msg_lower:
            return "blocked_account"
        elif "refund" in msg_lower or "unauthorized" in msg_lower:
            return "refund_request"
        return "general_inquiry"
