import logging
import gradio as gr
import warnings
from super_res_gan import main

logging.basicConfig(level=logging.INFO)

warnings.filterwarnings("ignore", category=UserWarning,
                        message=".*?Your .*? set is empty.*?")
demo = gr.Blocks(title='Super Resolution GAN Demo')  # Create a gradio block


with demo:
    gr.Markdown("# Super Resolution GAN Demo")
    with gr.Tabs():
        with gr.TabItem("Examples"):  # If the user wants to use the examples
            with gr.Row():
                rad1 = gr.components.Radio(
                    ['Image 1', 'Image 2'], label='Select Low Resolution Image and wait till it appears!')  # Radio button to select the image
                img1 = gr.Image(label="Low Resolution Image Example", shape=(300, 300))
            submit1 = gr.Button('Submit')
        with gr.TabItem("Do it yourself!"):  # If the user wants to add their own image
            with gr.Row():
                img3 = gr.Image(
                    label="Add any Low resolution image", shape=(300, 300))
            submit2 = gr.Button('Submit')

        def action1(choice):  # Function to show the article when the user selects the article
            global filepath
            if choice == 'Image 1':
                filepath = './SRGAN/samples/comic_lr.png'
                return './SRGAN/samples/comic_lr.png'
            elif choice == 'Image 2':
                filepath = './SRGAN/samples/pika.jpeg'
                return './SRGAN/samples/pika.jpeg'

        # Change the image when the user selects the image name
        rad1.change(action1, rad1, img1)

        # Output for the Highlighted text
        op = gr.Image(label="High Res Image", shape=(300, 300))

        gr.Markdown(
            "### Made with ❤️ by Arsh using TrueFoundry's Gradio Deployment")
        gr.Markdown(
            "### [Github Repo](https://github.com/d4rk-lucif3r/Super-Resolution-GAN-Demo)")
        gr.Markdown(
            '### [Blog]()')

        def fn(img1):  # Main function
            global filepath
            result = main(filepath)
            return result

        try:
            submit1.click(fn=fn, outputs=[
                op], inputs=[img1])  # Submit button for the examples
        except Exception as e:
            logging.info('Error in submit1 ', e)
            pass
        # Submit button for the user input
        submit2.click(fn=fn, outputs=[op], inputs=[img1])
        
        
# demo.queue()  # Queue the block
demo.launch(server_port=8080, server_name='0.0.0.0',
            show_error=True)  # Launch the gradio block
