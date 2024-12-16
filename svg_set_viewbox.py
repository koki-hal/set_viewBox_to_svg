"""
The svg file genarated by PowerPoint doesn't have viewBox attribute.

This script spcifies viewBox attribute by using width and height values.
The width and height values are removed instead adding viewBox.

ex.
  befor modify : <svg width="1234" height="789" ... >
  after modify : <svg viewBox="0 0 1234 789" ... >
"""

import os
import shutil

def get_svg_block(block):
    """
    Return the start and end index of <svg ...> block
    """

    start = -1
    end = -1

    # search '<svg'
    start = block.find('<svg ')
    if start == -1:
        return start, end

    # search '>'
    end = block.find('>', start+1)
    if end == -1:
        return start, end

    return start, end+1


def split_with_quote(block, separator=' '):
    """
    Append to list after splitting block with specified separator.
    If the separator is in the quote, it is not considered as a separator.
    """

    item_list = []
    n = 0  # search index
    while block:
        # search single quote and double quote
        sq1 = block[n:].find("'")
        dq1 = block[n:].find('"')

        # if a quote is found, find the closing quote
        if sq1 != -1:
            sq2 = block[n+sq1+1:].find("'")
            sq2 = sq1 + 1 + sq2
        
        if dq1 != -1:
            dq2 = block[n+dq1+1:].find('"')
            dq2 = dq1 + 1 + dq2

        # search separator
        sp = block[n:].find(separator)

        if sp == -1:
            # finish searching to the end
            item_list.append(block)
            break

        elif sq1 != -1 and (sq1 < sp and sp < sq2):
            # separator is in single quote
            
            # set the search index to just after the quote
            n = sq2+1
            # search again
        
        elif dq1 != -1 and (dq1 < sp and sp < dq2):
            # separator is in double quote
            
            # set the search index to just after the quote
            n = dq2+1
            # search again

        else:
            # separator is not in the quote

            # Append the part of the block up to the separator to the list (don't forget to add the search index)
            item_list.append(block[0:n+sp])

            # update the block for search
            block = block[n+sp+1:]
            # reset the search index
            n = 0

    return item_list


def parse_svg_block(block):
    """
    Parse the '<svg ...>' to dict
    """

    svg_dict = {}

    # pick up just after '<svg' part
    block = block[5:-1]

    # split block with space (considering quotes)
    items = split_with_quote(block, ' ')

    # parse items to dict (key="value" forms)
    for item in items:
        key, value = item.split('=')
        svg_dict[key] = value

    return svg_dict


def get_width(svg_dict):
    """
    Pick up width from dict
    """

    w = svg_dict['width'].strip('"')
    return w


def get_height(svg_dict):
    """
    Pick up height from dict
    """

    h = svg_dict['height'].strip('"')
    return h


def main(svg_src, svg_dst):
    # load original SVG file
    with open(svg_src, 'r', encoding='UTF-8') as file:
        svg = file.read()

    # search '<svg ... >'
    start, end = get_svg_block(svg)

    # copy the part before '<svg' to a save variable
    svg_out = svg[0:start]

    # pick up '<svg ... >' block
    svg_block = svg[start:end]

    # parse '<svg ... >' block to dict
    svg_dict = parse_svg_block(svg_block)

    # if there is viewBox already, do nothing
    if 'viewBox' in svg_dict:
        return

    # if there is no width and height attributes, do nothing
    if 'width' not in svg_dict or 'height' not in svg_dict:
        return

    # pick up width and height
    width = get_width(svg_dict)
    height = get_height(svg_dict)

    # remove width and height from dict
    del svg_dict['width']
    del svg_dict['height']

    # generate viewBox
    viewbox = f'viewBox="0 0 {width} {height}"'

    # generate new '<svg' block with viewBox
    svg_block_new = f'<svg {viewbox}'
    # enumerate dict and append
    for key, value in svg_dict.items():
        # append item
        svg_block_new += f' {key}={value}'
    # append '>'
    svg_block_new += '>'

    # add new '<svg' block to the valiable to save
    svg_out += svg_block_new

    # add the part after '<svg' to the valiable to save
    svg_out += svg[end:]

    # save to the file
    with open(svg_dst, 'w', encoding='UTF-8') as file:
        file.write(svg_out)

    print(svg_dst)

    pass


if __name__ == '__main__':
    # processing all *.svg files in the current directory
    for svg in os.listdir('.'):
        if svg.endswith('.svg'):
            # print(svg)
            main(svg, svg)  # overwrite

