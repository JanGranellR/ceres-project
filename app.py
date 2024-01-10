import os
from config import config
import joblib
import cv2 as cv
import numpy as np
import gradio as gr

def run(image):
    """
    Define the main function to run the models on the input image
    """

    # Prepare the image
    image = np.array(image)
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    image = cv.resize(image, (50, 50))
    image = image.flatten()

    data = {}

    for model_file in os.listdir(os.path.join(config.model["path"], config.model["path_models"])):
        # Load the pre-trained model
        model = joblib.load(os.path.join(config.model["path"], config.model["path_models"], model_file))

        # Make predictions using the model
        results = model.predict_proba([image])[0]

        # Find the index of the label that is not "other"
        non_other_index = np.where(model.classes_ != 'other')[0][0]

        # Populate data for bar plot
        data[model.classes_[non_other_index]] = results[non_other_index]
    
    return data

if __name__ == '__main__':
    # Define examples
    examples = [os.path.join("test", filename) for filename in os.listdir("test")]

    # Create a Gradio interface with examples
    iface = gr.Interface(
        title = "Ceres Project",
        fn = run,
        inputs = gr.Image(type = "pil"),
        outputs = gr.Label(),
        allow_flagging = "never",
        examples = examples
    )

    # Launch the Gradio interface
    iface.launch(share = True, server_name = "0.0.0.0")
