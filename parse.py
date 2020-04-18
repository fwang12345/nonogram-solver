import cv2
from pytesseract import image_to_string, pytesseract
# Process image and return processed image along with bounding rectanges of rows and columns digits
def preprocess(fname):
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    ref = cv2.imread(fname)
    # Convert to black and white
    ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    ref = cv2.threshold(ref, 226, 255, cv2.THRESH_BINARY_INV)[1]
    # Find Contours
    refCnts, hierarchy = cv2.findContours(ref.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    sort = sorted(refCnts, key=cv2.contourArea, reverse=True)

    # Crop image
    x, y, _, h = cv2.boundingRect(sort[0])
    lower = y+h
    width = len(ref[0])
    ref = ref[lower-width:lower, 0:width]
    #cv2.imwrite('process.png', ref)
    # Crop digits
    refCnts, hierarchy = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    bound = [cv2.boundingRect(c) for c in refCnts]
    rows = [rect for rect in bound if rect[0] < x and rect[0] > 0]
    rows = sorted(rows, key=lambda k: [k[1], k[0]])
    cols = [rect for rect in bound if rect[1] < width-h and rect[1] > 0]
    cols = sorted(cols, key=lambda k: [k[0], k[1]])
    return ref, rows, cols

# Parse pattern given processed image and boundign boxes
def get_patterns(ref, rows, cols):
    thres = 150
    #print('Rows')
    space = 0
    i = 0
    align = []
    while i < len(rows):
        row = [rows[i]]
        i += 1
        while (i < len(rows) and rows[i][1] < rows[i-1][1] + rows[i-1][3]):
            row.append(rows[i])
            i += 1
        row = sorted(row, key=lambda k:k[0])
        align.append(row)
        if (len(row) > 1):
            dx = max([row[j][0] - row[j-1][0] - row[j-1][2] for j in range(1, len(row))])
            if (dx > space):
                space = dx
    for i, row in enumerate(align):
        j = 0
        new = []
        while (j < len(row)):
            group = [row[j]]
            k = j + 1
            while (k < len(row) and row[k][0] - row[k-1][0] - row[k-1][2] < space / 2):
                group.append(row[k])
                k += 1
            new.append(group)
            j = k
        align[i] = new
    row_digits = []
    for i, row in enumerate(align):
        digits = []
        for j, group in enumerate(row):
            number = ''
            l = len(group)
            for k, rect in enumerate(group):
                x, y, w, h = rect
                border = 1
                digit = ''
                box = ref[y:y+h,x:x+w]
                box = cv2.threshold(box, 0, 255, cv2.THRESH_BINARY_INV)[1]
                box = cv2.resize(box, (w * 30, h * 30))
                box = cv2.threshold(box, thres, 255, cv2.THRESH_BINARY)[1]
                while (border < 10 and len(digit) == 0):
                    box = cv2.copyMakeBorder(box, 30, 30, 30, 30, cv2.BORDER_CONSTANT, value = (255, 255, 255))
                    #cv2.imwrite(r'digits\row%d-%d-%d.png' %(i, j, k), box)
                    digit = image_to_string(box, config="--psm 13 -c tessedit_char_whitelist=0123456789")
                    border += 1
                #print("Number (border=%d) at row %d group %d digit %d is %s" %(border-1, i, j, k, digit))
                number += digit
            if len(number) != l and l > 1:
                number = ''
                upper = min(group[0][1], group[l-1][1])
                lower = max(group[0][1] + group[0][3], group[l-1][1] + group[l-1][3])
                y = upper
                w = group[l-1][0] + group[l-1][2] - group[0][0]
                h = lower - upper
                box = ref[y:y+h,x:x+w]
                box = cv2.threshold(box, 0, 255, cv2.THRESH_BINARY_INV)[1]
                box = cv2.resize(box, (w * 30, h * 30))
                box = cv2.threshold(box, thres, 255, cv2.THRESH_BINARY)[1]
                border = 1
                while (border < 10 and len(number) == 0):
                    box = cv2.copyMakeBorder(box, 30, 30, 30, 30, cv2.BORDER_CONSTANT, value = (255, 255, 255)) 
                    #cv2.imwrite(r'digits\row%d-%d.png' %(i, j), box)
                    number = image_to_string(box, config="--psm 13 -c tessedit_char_whitelist=0123456789")
                    border += 1
            #print("Number (border=%d) at row %d group %d is %s" %(border-1, i, j, number))
            digits.append(int(number))
            
        row_digits.append(digits)
    #print('Columns')
    space = max([cols[i][0] - cols[i-1][0] - cols[i-1][2] for i in range(1, len(cols))])
    i = 0
    align = []
    while i < len(cols):
        col = [cols[i]]
        i += 1
        while (i < len(cols) and cols[i][0] - cols[i-1][0] + cols[i-1][2] < space / 2):
            col.append(cols[i])
            i += 1
        col = sorted(col, key=lambda k:k[1])
        new = []
        j = 0
        while (j < len(col)):
            group = [col[j]]
            k = j + 1
            while (k < len(col) and col[k][1] < col[k-1][1] + col[k-1][3]):
                k += 1
            group = sorted(col[j:k], key=lambda key:key[0])
            new.append(group)
            j = k
        align.append(new)
    col_digits = []
    for i, col in enumerate(align):
        digits = []
        for j, group in enumerate(col):
            number = ''
            l = len(group)
            for k, rect in enumerate(group):
                x, y, w, h = rect
                border = 1
                digit = ''
                box = ref[y:y+h,x:x+w]
                box = cv2.threshold(box, 0, 255, cv2.THRESH_BINARY_INV)[1]
                box = cv2.resize(box, (w * 30, h * 30))
                box = cv2.threshold(box, thres, 255, cv2.THRESH_BINARY)[1]
                while (border < 10 and len(digit) == 0):
                    box = cv2.copyMakeBorder(box, 30, 30, 30, 30, cv2.BORDER_CONSTANT, value = (255, 255, 255))
                    #cv2.imwrite(r'digits\col%d-%d-%d.png' %(i, j, k), box)
                    digit = image_to_string(box, config="--psm 13 -c tessedit_char_whitelist=0123456789")
                    border += 1
                #print("Number (border=%d) at col %d group %d digit %d is %s" %(border-1, i, j, k, digit))
                number += digit
            if len(number) != l and l > 1:
                number = ''
                upper = min(group[0][1], group[l-1][1])
                lower = max(group[0][1] + group[0][3], group[l-1][1] + group[l-1][3])
                y = upper
                w = group[l-1][0] + group[l-1][2] - group[0][0]
                h = lower - upper
                box = ref[y:y+h,x:x+w]
                box = cv2.threshold(box, 0, 255, cv2.THRESH_BINARY_INV)[1]
                box = cv2.resize(box, (w * 30, h * 30))
                box = cv2.threshold(box, thres, 255, cv2.THRESH_BINARY)[1]
                border = 1
                while (border < 10 and len(number) == 0):
                    box = cv2.copyMakeBorder(box, 30, 30, 30, 30, cv2.BORDER_CONSTANT, value = (255, 255, 255)) 
                    #cv2.imwrite(r'digits\col%d-%d.png' %(i, j), box)
                    number = image_to_string(box, config="--psm 13 -c tessedit_char_whitelist=0123456789")
                    border += 1
            #print("Number (border=%d) at col %d group %d is %s" %(border-1, i, j, number))
            digits.append(int(number))
        col_digits.append(digits)
    if (len(row_digits) != len(col_digits)):
        for i in row_digits:
            print(i)
        print('-----------------')
        for i in col_digits:
            print(i)
        raise Exception('Number of rows does not match number of columns')
    return len(row_digits), row_digits, col_digits