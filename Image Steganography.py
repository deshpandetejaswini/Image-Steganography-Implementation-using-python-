# Python program implementing Image Steganography
# PIL module is used to extract
# pixels of image and modify it

#from PIL import Image
import tkinter as tk

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):

        # list of binary codes
        # of given data
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))  # 08b types 0 in first 4 places of binary code 
            #ord() function returns the Unicode code from a given character
        return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata._next_()[:3] +
                                imdata._next_()[:3] +
                                imdata._next_()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        #yield returns the value from function 
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)   #Image in 2D 
    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image
def encode():
    global Ekey
    Ekey=int(input("Enter the security key : "))
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
    global data
    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def decode():
    Dkey=int(input("Enter the security key to decode your message :"))
    if(Dkey==Ekey):
        img = input("Enter image name(with extension) : ")
        image = Image.open(img, 'r')

        data = ''
        imgdata = iter(image.getdata())

        while (True):
            pixels = [value for value in imgdata._next_()[:3] +
                                imgdata._next_()[:3] +
                                imgdata._next_()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            print("Data decoded : " ,data)
            return data

# Main Function
def main():

    root =tk.Tk()
    root.title(" GUI ")
    root.geometry("300x300")
    w = tk.Canvas(root, width=300, height=200)
    Label1=tk.Label(root,text = ":: Welcome to Steganography ::",bg="Yellow").grid(row=1,column=1)
    entry1=tk.Entry(root)
    entry2=tk.Entry(root)
    button1= tk.Button(text='ENCODE', command = lambda : encode(), bg='green', fg='white', width= 40).grid(row=2,column=1)
   
    button2= tk.Button(text='DECODE', command = lambda : decode(), bg='green', fg='white', width= 40).grid(row=3,column=1)
    '''data=tk.Label(root,text="Data to be hided :")
    data.grid(row=4,column=1)
    global dataentry
    datavalue= tk.StringVar()
    dataentry=tk.Entry(root,textvariable=datavalue)
    dataentry.grid(row=4,column=2)'''
    
   
    root.mainloop()
    '''else:
        raise Exception("Enter correct input")
        ch = int(input("Enter 1 to continue: "))  
        if(ch != 1):
            print("Exited successfuly!! ")'''
       

# Driver Code
if _name_ == '_main_' :

    # Calling main function
    main()
