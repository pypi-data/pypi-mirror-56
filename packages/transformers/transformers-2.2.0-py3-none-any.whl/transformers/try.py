from transformers import TFBertModel
import tensorflow as tf

model = TFBertModel.from_pretrained("bert-base-cased")

input_ids = tf.constant([[1,2,3]])

wte = model.get_input_embeddings()
x = wte(input_ids, mode="embedding")
# inputs_dict["inputs_embeds"] = x
# outputs = model(inputs_dict)