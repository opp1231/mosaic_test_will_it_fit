%matplotlib widget

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Button, Slider
import matplotlib.patches as patches
plt.close()
efl_det = 1.9
efl_ex = 5.5
angle = 32.45*2*np.pi/360
angle2 = np.pi/2 -angle
det_win = 4.7
det_angle = 38*2*np.pi/360
ex_win = 6.2
ex_angle = 58*2*np.pi/360
len1 = 3



fig, ax = plt.subplots(figsize=(10,10))
ax.axis('equal')
ax.set_title("")

fig.subplots_adjust(left=0, bottom=0.3)
plt.title("MOSAIC ExM Gel Size")


x_detEFL, y_detEFL = [0, np.sin(angle)*efl_det], [0, np.cos(angle)*efl_det]
x_exEFL, y_exEFL = [0, -np.sin(angle2)*efl_ex], [0, np.cos(angle2)*efl_ex]

x_detWin = [x_detEFL[1]-det_win/2*np.cos(angle),x_detEFL[1]+det_win/2*np.cos(angle)]
y_detWin = [y_detEFL[1]+det_win/2*np.sin(angle),y_detEFL[1]-det_win/2*np.sin(angle)]

x_exWin = [x_exEFL[1]+ex_win/2*np.cos(angle2),x_exEFL[1]-ex_win/2*np.cos(angle2)]
y_exWin = [y_exEFL[1]+ex_win/2*np.sin(angle2),y_exEFL[1]-ex_win/2*np.sin(angle2)]

x_detWall1 = [x_detWin[1],x_detWin[1]+len1*np.cos(det_angle-angle)]
y_detWall1 = [y_detWin[1],y_detWin[1]+len1*np.sin(det_angle-angle)]

x_detWall2 = [x_detWin[0],x_detWin[0]-len1*2*np.cos(det_angle+angle)]
y_detWall2 = [y_detWin[0],y_detWin[0]+len1*2*np.sin(det_angle+angle)]

x_exWall1 = [x_exWin[1],x_exWin[1]-len1*np.cos(ex_angle-angle2)]
y_exWall1 = [y_exWin[1],y_exWin[1]+len1*np.sin(ex_angle-angle2)]

x_exWall2 = [x_exWin[0],x_exWin[0]-len1*np.cos(np.pi - ex_angle-angle2)]
y_exWall2 = [y_exWin[0],y_exWin[0]+len1*np.sin(np.pi - ex_angle-angle2)]

def det_obj_face(x):
    return y_detWin[0] + (y_detWin[1]-y_detWin[0])/(x_detWin[1]-x_detWin[0])*(x - x_detWin[0])

def det_obj_face_x(y):
    return (y - y_detWin[0])*(x_detWin[1]-x_detWin[0])/(y_detWin[1]-y_detWin[0]) + x_detWin[0]

def exc_obj_face(x):
    return y_exWin[0] + (y_exWin[1]-y_exWin[0])/(x_exWin[1]-x_exWin[0])*(x - x_exWin[0])

def det_obj_wall(x):
    return y_detWall2[0] + (y_detWall2[1]-y_detWall2[0])/(x_detWall2[1]-x_detWall2[0])*(x - x_detWall2[0])

obj_assembly = ax.plot(x_detEFL,y_detEFL,'k--',x_exEFL,y_exEFL,'k--',x_detWin,y_detWin,'k',x_exWin,y_exWin,'k',x_detWall1,y_detWall1,'k',x_detWall2,y_detWall2,'k',x_exWall1,y_exWall1,'k',x_exWall2,y_exWall2,'k')
def f(t,height):
    return  0 * t + height

t = np.linspace(-10, 6, 1000)

line, = ax.plot(t, f(t,0),'k')
rect = patches.Rectangle((0,0),1,1)
rect_im = patches.Rectangle((0,0),1,1)
rect.set_color('.8')
rect_im.set_color('g')
rect_im.set_lw(0)
rect.set_lw(0)
ax.add_patch(rect)
ax.add_patch(rect_im)

# Make a vertically oriented slider to control the amplitude
axcvslip = fig.add_axes([0.25, 0.3, 0.65, 0.03])
cvslip_slider = Slider(
    ax=axcvslip,
    label="Coverslip Height (mm)",
    valmin=-2,
    valmax=0,
    valinit=0
)

# Make a vertically oriented slider to control the amplitude
axrect_height = fig.add_axes([0.25, 0.2, 0.65, 0.03])
rect_height_slider = Slider(
    ax=axrect_height,
    label="Gel Height (mm)",
    valmin=0.01,
    valmax=5,
    valinit=1
)

# Make a vertically oriented slider to control the amplitude
axrect_width = fig.add_axes([0.25, 0.1, 0.65, 0.03])
rect_width_slider = Slider(
    ax=axrect_width,
    label="Gel width (mm)",
    valmin=0.01,
    valmax=10,
    valinit=1
)

axrect_position = fig.add_axes([0.25, 0, 0.65, 0.03])
rect_pos_slider = Slider(
    ax=axrect_position,
    label="Gel X Position (mm)",
    valmin=-10,
    valmax=5,
    valinit=0
)


text_init = '\n'.join(("Portion of Gel Available to Image",
"Height: " + str(rect_im.get_height()) + " mm",
"Width: " + str(rect_im.get_width()) + " mm"))

textbox = ax.text(.01, 0.98, text_init, transform=ax.transAxes, fontsize=14,
        verticalalignment='top')


# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(f(t,cvslip_slider.val))
    rect.set_y(cvslip_slider.val)
    rect.set_x(rect_pos_slider.val)
    rect.set_height(rect_height_slider.val)
    rect.set_width(rect_width_slider.val)


    if 0 < rect.get_corners()[2,1] < rect_height_slider.val:
        rect_im.set_height(rect.get_corners()[2,1])
        rect_im.set_y(0)
    elif rect.get_corners()[2,1]>0:
        rect_im.set_height(rect_height_slider.val)
        rect_im.set_y(0)
    else:
        rect_im.set_height(0)
        rect_im.set_y(0)
    if rect_width_slider.val > det_obj_face_x(rect.get_corners()[2,1])>0:
        rect_im.set_width(det_obj_face_x(rect.get_corners()[2,1]))
        rect_im.set_x(rect.get_corners()[2,0] - det_obj_face_x(rect.get_corners()[2,1]))
    elif det_obj_face_x(rect.get_corners()[2,1]) > rect_width_slider.val:
        rect_im.set_width(rect_width_slider.val)
        rect_im.set_x(rect_pos_slider.val)
    else:
        rect_im.set_width(0)
        rect_im.set_height(0)

    if rect.get_corners()[2,1]<= y_detWin[1] and rect.get_corners()[3,1] <= y_exWin[1]:
        rect_im.set_y(cvslip_slider.val)
        rect_im.set_x(rect_pos_slider.val)
        rect_im.set_height(rect_height_slider.val)
        rect_im.set_width(rect_width_slider.val)
        
    if det_obj_face(rect.get_corners()[2,0]) <= rect.get_corners()[2,1] and x_detWin[0] < rect.get_corners()[2,0] < x_detWin[1]:
        rect.set_color('r')
        rect_im.set_color('r')
        textbox.set_text("Your gel is hitting an objective!")
    elif rect.get_corners()[2,1] >+ y_detWin[1] and rect.get_corners()[2,0] > x_detWin[1]:
        rect.set_color('r')
        rect_im.set_color('r')
        textbox.set_text("Your gel is hitting an objective!")
    elif exc_obj_face(rect.get_corners()[3,0]) <= rect.get_corners()[3,1] and x_exWin[1] < rect.get_corners()[3,0] < x_exWin[0]:
        rect.set_color('r')
        rect_im.set_color('r')
        textbox.set_text("Your gel is hitting an objective!")
    elif det_obj_wall(rect.get_corners()[2,0]) <= rect.get_corners()[2,1] and x_detWall2[1] < rect.get_corners()[2,0] < x_detWall2[0]:
        rect.set_color('r')
        rect_im.set_color('r')
        textbox.set_text("Your gel is hitting an objective!")
    elif rect.get_corners()[3,1] > y_exWin[1] and rect.get_corners()[3,0] < x_exWin[1]:
        rect.set_color('r')
        rect_im.set_color('r')
        textbox.set_text("Your gel is hitting an objective!")
    else:
        rect.set_color('0.8')
        rect_im.set_color('g')
        textbox.set_text('\n'.join(("Portion of Gel Available to Image",
        "Height: " + str(np.round(rect_im.get_height(),decimals=2)) + " mm",
        "Width: " + str(np.round(rect_im.get_width(),decimals=2)) + " mm")))
    
    fig.canvas.draw_idle()


# register the update function with each slider
#cvslip_slider.on_changed(update)
rect_height_slider.on_changed(update)
rect_width_slider.on_changed(update)
rect_pos_slider.on_changed(update)
plt.show()