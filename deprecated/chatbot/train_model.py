<<<<<<< HEAD
#%%
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
path = "data.txt"

# Load the GPT-2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

#%%
# Load the GPT-2 model architecture
model = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id)

# Load your dataset and tokenize it
dataset = TextDataset(tokenizer=tokenizer, file_path=path, block_size=128)

# Use a DataCollator to handle batching and padding of the data
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
data_collator



# Define the training arguments
training_args = TrainingArguments(
    output_dir='./results',
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=16,
    save_total_limit=2
)


# Create the Trainer instance and start training
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator
)
trainer
#%%
trainer.train()


#%%

# Generate some text using the trained model
generated_text = model.generate(
    input_ids=tokenizer.encode("chat gpt large language model?", return_tensors='pt'),
    max_length=50,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.7,
    num_return_sequences=1
)



# Decode the generated output and print it
output_text = tokenizer.decode(generated_text[0], skip_special_tokens=True)
print(output_text)


# %%
=======
version https://git-lfs.github.com/spec/v1
oid sha256:797c952cfdc4494e6cc7eaeb7554f1ae2abf35c2fd0ec91b38543d5fc4a8e46d
size 1543
>>>>>>> c8e2e909f17e07eb3b555579bdfb11e9a874eb1f
