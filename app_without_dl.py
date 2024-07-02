from livewire import Trackmanager
from PIL import Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# from dl_utils import Dlseg
# from torchvision import models
import os
import time


INTERACTIVE = True  # to compute interactive shortest path suggestions
editmode = False
start_point = None
file_loc = []
file_cursor = 0
w = 0
length_penalty = 10.0
seg_object_name = 'example'

# prepare deep learning(This version does not use deep learning model, can run faster)
# seg_model = Dlseg(models.segmentation.deeplabv3_resnet50(pretrained=True))
seg_model = None
# readfile
while True:
    loc=input("Drag your picture folder dir here(special UTF-8 in path is not availiable)->")
    loc=loc.replace("\\","/")
    loc=loc.replace("\"","")

    for pic_files in os.listdir(loc):
        _,ext = os.path.splitext(pic_files)
        # find all files with avi ext
        if ext == '.jpg' or ext == '.JPG' or ext == '.png' or ext == '.PNG' or ext == '.tif' or ext == '.TIF':
            file_loc.append(os.path.join(loc,pic_files))
    
    if file_loc!=[]:
        break

def openfiles(img_loc):
    image = Image.open(img_loc)
    global w
    w, h = image.size
    resize_factor = max(w,h)/480
    image = image.resize((int(w//resize_factor),int(h//resize_factor)))
    return image

def savefile():
    global seg_object_name,image,track,file_loc,file_cursor
    txt_name,_ = os.path.splitext(file_loc[file_cursor])
    txt_name += '.txt'
    global w
    w1, _ = image.size
    resize_factor = w/w1
    path = track.get_path()
    if path == []:
        return
    path1 = list(zip(np.array(path)[:,1]*resize_factor, np.array(path)[:,0]*resize_factor))
    with open(txt_name, 'w') as fv:
        fv.write(seg_object_name+'\n')
        fv.write(str(image.size)+'\n')
        fv.write('---'+'\n')
        for points in path1:
            fv.write(str(points)+'\n')  

def savedots():
    global file_loc,file_cursor
    txt_name,_ = os.path.splitext(file_loc[file_cursor])
    txt_name += '.txt'
    with open(txt_name, 'w') as fv:
        for i, poly in enumerate(track.Polygon_list):
            fv.write(f'======================== segment {i} ==========================\n')
            path = track.get_multi_path(poly)
            path = list(path)
            # path1 = list(zip(np.array(path)[:,1], np.array(path)[:,0]))
            for points in path:
                fv.write(str(points)+'\n')  
        
def nextfile():
    global image,track,file_loc,file_cursor
    savefile()
    if (file_cursor+1)>=len(file_loc):
        return
    else:
        file_cursor+=1
        image = openfiles(file_loc[file_cursor])
        time0 = time.process_time()
        track = Trackmanager(image,dl_util=seg_model,step=20)
        track.img_size = image.size
        # print(time.process_time()-time0)

def lastfile():
    global image,track,file_loc,file_cursor
    savefile()
    if (file_cursor)<=0:
        return
    else:
        file_cursor-=1
        image = openfiles(file_loc[file_cursor])
        track = Trackmanager(image,dl_util=seg_model,step=20)
        track.img_size = image.size

def create_mask():
    print(track.img_size)
    mask = np.zeros((track.img_size[1], track.img_size[0]))
    if not editmode and (track.Polygon_list is not None):
        fig_mask, ax_mask = plt.subplots()
        ax_mask.set_axis_off()
        ax_mask.imshow(mask, cmap='gray')  # Display the mask
        for poly in track.Polygon_list:
            path = track.get_multi_path(poly)
            path = list(path)
            polygons = list(zip(np.array(path)[:,1], np.array(path)[:,0]))
        # for polygon_nodes in track.Polygon_list:
            polygon = plt.Polygon(polygons, closed=True, edgecolor='white', facecolor='white')
            ax_mask.add_patch(polygon)

        
        image_filename = 'output_plot_with_filled_polygons.png'
        current_directory = os.getcwd()
        print(current_directory)
        image_path = os.path.join(current_directory, image_filename)
        fig_mask.savefig(image_path, dpi=300, bbox_inches='tight', pad_inches=0)
        # plt.show()
        print('Mask saved successfully.')


image = openfiles(file_loc[file_cursor])
track = Trackmanager(image,dl_util=seg_model,step=20)
track.img_size = image.size
plt.gray()

# -------------------------------------------------------------- #
def refresh_frame(rescale = False):
    path = track.get_path() # [(r,c),(),...]
    seeds = track.get_seeds()
    # print(path)
    xy_scale = plt.axis()
    plt.clf()
    # plt.imshow(track.algorithm.edges)
    plt.imshow(image)
    if path!= []:
        plt.plot(np.array(path)[:,1], np.array(path)[:,0], '-g')
    if seeds!=[]:
        plt.scatter(np.array(seeds)[:,1], np.array(seeds)[:,0], marker='x', c='b')
    plt.title(file_loc[file_cursor],fontsize = 6)
    plt.draw()
    if not rescale:
        plt.axis(xy_scale)      # hold previous scale

def quit_edit():
    if editmode and (track.start_point is not None):
        track.close_poly()
        refresh_frame()
        path = track.get_path()
        path = list(path)
        path1 = list(zip(np.array(path)[:,1], np.array(path)[:,0]))
        p = plt.Polygon(path1,color='white',alpha=0.4)
        plt.gca().add_patch(p)
        plt.draw()

def draw_multi_poly():
        
    for poly in track.Polygon_list:
        path = track.get_multi_path(poly)
        path = list(path)
        path1 = list(zip(np.array(path)[:,1], np.array(path)[:,0]))
        p = plt.Polygon(path1,color='white',alpha=0.4)
        plt.gca().add_patch(p)
        plt.draw()

        

def back_step():
    track.back_step()
    try:
        plt.pause(0.2)
    except:
        pass
    refresh_frame()

# -------------------------------- #

def button_pressed(event):
    global editmode
    if not editmode:
        return
    if track.start_point is None:
        start_point = (int(event.ydata), int(event.xdata))
        track.set_start(start_point)
    else:
        end_point = (int(event.ydata), int(event.xdata))
        track.update_points(end_point)
        refresh_frame()


def mouse_moved(event):
    global editmode
    if not editmode:
        return
    if track.start_point is None:
        return
    if (event.ydata is None) or (event.xdata is None):
        return
    
    end_point = (int(event.ydata), int(event.xdata))
    # the line below is calling the segmentation algorithm
    path,ref = track.add_tmp_path(end_point)
    plt.plot(np.array(path)[:,1], np.array(path)[:,0], '-r') 
    plt.draw()
    if ref:
        refresh_frame()

def key_pressed(event):
    global editmode
    if event.key == ' ':
        if track.start_point is not None:
            track.close_poly()
            track.Polygon_list.append(track.all_points_list)
            track.clear()
            refresh_frame()
            draw_multi_poly()
        else:
            quit_edit()
        editmode = ~editmode


    if event.key == 'c':
        track.clear()
        refresh_frame()

    if (not editmode) and event.key == 'a':
        lastfile()
        refresh_frame(rescale=True)

    if (not editmode) and event.key == 'd':
        nextfile()
        refresh_frame(rescale=True)
    
    if (not editmode) and event.key == 'p':
        savedots()

    if event.key == 'm':
        create_mask()

    if not editmode:
        return
    # the following keys only work in edit mode
    if event.key == 'b':
        quit_edit()
        track.close_poly()
        track.Polygon_list.append(track.all_points_list)
        track.clear()

    elif event.key == 's':
        if not editmode:
            plt.savefig('output_plot.png')

    elif event.key == 'backspace' :
        back_step()
        # print("Back one seed")


print("=========  Instruction  ==========")
print("# When not editing:") 
print("key: A           Switch to last pic, and save track") 
print("key: D           Switch to next pic, and save track") 
print("key: space       Begin editing") 
print("# When editing:") 
print("key: space           second time: Exit editing and confirm(AUTO close polygon)") 
print("mouse: Left button   Begin/Add a key point") 
print("mouse: Move          Auto fit a curve") 
print("key: esc             Exit editing") 
print("key: C               Clear curves on canvas")
print("key: b               next curve")
print("key: s               Save the image")
print("key: m               Create mask")
 
  
plt.connect('button_release_event', button_pressed)
if INTERACTIVE:
    plt.connect('motion_notify_event', mouse_moved)
plt.connect('key_press_event', key_pressed)

plt.imshow(image)
plt.autoscale(False)
plt.title('Livewire seg tool')
plt.show()


