import os 
import imageio

def make_gif(image_names, folder_path, gif_name = 'demogif.gif', n_frames = 10):
  with imageio.get_writer(gif_name, mode='I') as writer:
    for filename in image_names:
        image = imageio.imread(folder_path + filename)
        for i in range(n_frames):
            writer.append_data(image)

def main():
    img_folder_path = 'ECEMasterProject/RL/imgs/' 
    image_names = os.listdir(img_folder_path)
    image_names = [k for k in image_names if 'png' in k]
    print(image_names)
    make_gif(image_names, img_folder_path)


if __name__ == '__main__':
    main()