#%%
import textract

# Extract text from PDF file
text = textract.process('2022 Loan History.pdf')

# Print the text
print(text.decode('utf-8'))


# %%
