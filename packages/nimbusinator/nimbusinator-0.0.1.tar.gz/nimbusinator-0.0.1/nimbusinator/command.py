from nimbusinator.tools import message, fatal, is_valid_colour, colour_to_bgr, fix_coord, colrows_to_xy
from nimbusinator.tools import plonk_image, plonk_transparent_image, colour_char
import numpy as np
import cv2
import time

class Command:
    """Nimbus commands

    This class contains the commands to control the Nimbus display.  The commands
    mimick the syntax found in RM Basic but re-written Pythonically.  In creating an 
    object of this class it must be bound to a pre-existing Nimbus object.  It is
    highly recommended to read the original Nimbus manuals (particularly RM Basic)
    to get a deeper understanding of how these commands originally worked.

    Args:
        nimbus (Nimbus): The Nimbus object to bind to

    """

    def __init__(self, nimbus):
        """Create a new Command object

        In creating an object of this class it must be bound to
        a pre-existing Nimbus object.

        Args:
            nimbus (Nimbus): The Nimbus object to bind to
        
        """

        # Validate params
        # To avoid circular import we can't put Nimbus in isintance but we can
        # assert that the object contains a string called title.
        assert isinstance(nimbus.title, str), "Command object needs to be bound to a Nimbus object"
        self.nimbus = nimbus


    def cls(self):
        """Clear the screen of all text and graphics and reset cursor position

        """

        # Wipe screen data in the Nimbus and fill screen with paper colour. First
        # define a new PIL image to make sure it matches the current screen mode, 
        # e.g. if set_mode was just called
        screen_data = np.zeros((self.nimbus.screen_size[1]+1, self.nimbus.screen_size[0]+1, 3), dtype=np.uint8)
        cv2.rectangle(screen_data, (0,0), (self.nimbus.screen_size[0], self.nimbus.screen_size[1]), colour_to_bgr(self.nimbus, self.nimbus.paper_colour),-1)
        self.nimbus.update_screen(screen_data)


    def set_mode(self, columns):
        """Select either high-resolution or low-resolution screen mode

        In RM Basic the screen resolution was set by the number of columns: 
        40 for low-resolution and 80 for high-resolution.  Any other values
        has no effect.  Nimbusinator is more strict and will yield an error
        if any other values are entered.  Check the original RM Basic manual
        for a description of how screen resolutions worked on the Nimbus.
        High-resolution mode is particularly odd.

        Args:
            columns (int): The number of colums (40 or 80)

        """
        
        # validate params
        assert isinstance(columns, int), "The value of columns must be integer, not {}".format(columns)
        assert (columns == 80 or columns == 40), "The value of columns can be 80 or 40, not {}".format(columns)

        # change screen size and set default colours accordingly
        if columns == 80:
            self.nimbus.screen_size = (640, 250)
            self.nimbus.high_res_colours = self.nimbus.high_res_default_colours.copy()
            self.set_paper(0)
            self.set_border(0)
            self.set_brush(3)
            self.set_pen(3)
            self.set_curpos((1, 1))
            self.cls()
            return
        if columns == 40:
            self.nimbus.screen_size = (320, 250)
            self.nimbus.low_res_colours = self.nimbus.low_res_default_colours.copy()
            self.set_paper(0)
            self.set_border(0)
            self.set_brush(15)
            self.set_pen(15)
            self.set_curpos((1, 1))
            self.cls()
            return


    def set_cursor(self, flag):
        """Show or hide cursor

        Args:
            flag (boolean): True to show cursor, False to hide

        """
        
        # validate params
        assert isinstance(flag, bool), "The value of flag must be boolean, not {}".format(flag)

        self.nimbus.show_cursor = flag


    def plonk_logo(self, coord):
        """Plonk the RM Nimbus logo on screen

        Args:
            coord (tuple): The (x, y) position to plonk the logo

        """

        # validate params
        assert isinstance(coord, tuple), "The value of coord must be a tuple, not {}".format(coord)
        assert len(coord) == 2, "The coord tuple must have 2 values, not {}".format(len(coord))
        for i in range(0, 2):
            assert isinstance(coord[i], int), "This value in coord must be an integer, not{}".format(coord[i])

        screen_data = self.nimbus.get_screen()
        screen_data = plonk_image(self.nimbus, screen_data, self.nimbus.logo, coord)
        self.nimbus.update_screen(screen_data)


    def set_paper(self, colour):
        """Set the paper colour
        
        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)

        """

        # validate params
        assert isinstance(colour, int), "The value of colour must be an integer, not {}".format(type(colour))
        assert (colour == is_valid_colour(self.nimbus, colour)), "Colour {} is out-of-range for this screen mode".format(colour)

        self.nimbus.paper_colour = colour
        
    
    def set_colour(self, colour1, colour2):
        """Set a colour to a new colour

        Args:
            colour1 (int): The colour code to be changed
            colour2 (int): The new colour to be assigned to colour1
        
        """

        # validate params
        assert isinstance(colour1, int), "The value of colour1 must be an integer, not {}".format(type(colour1))
        assert isinstance(colour2, int), "The value of colour2 must be an integer, not {}".format(type(colour2))
        assert (colour2 >= 0 and colour2 <= 15), "The value of colour 2 must be >= 0 and <= 15, not {}".format(colour2)
        assert (colour1 == is_valid_colour(self.nimbus, colour1)), "Colour1 {} is out-of-range for this screen mode".format(colour1)

        if self.nimbus.screen_size == (320, 250):
            self.nimbus.low_res_colours[colour1] = colour2
        if self.nimbus.screen_size == (640, 250):
            self.nimbus.high_res_colours[colour1] = colour2


    def set_border(self, colour):
        """Set the border colour
        
        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)
            
        """
 
        # validate params
        assert isinstance(colour, int), "The value of colour must be an integer, not {}".format(type(colour))
        assert (colour == is_valid_colour(self.nimbus, colour)), "Colour {} is out-of-range for this screen mode".format(colour)

        self.nimbus.border_colour = colour
    

    def set_brush(self, colour):
        """Set the brush colour
        
        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)
            
        """

        # validate params
        assert isinstance(colour, int), "The value of colour must be an integer, not {}".format(type(colour))
        assert (colour == is_valid_colour(self.nimbus, colour)), "Colour {} is out-of-range for this screen mode".format(colour)

        self.nimbus.brush_colour = colour


    def set_pen(self, colour):
        """Set the pen colour

        Args:
            colour (int): Colour value (High-resolution: 0-3, low-resolution: 0-15)
            
        """

        # validate params
        assert isinstance(colour, int), "The value of colour must be an integer, not {}".format(type(colour))
        assert (colour == is_valid_colour(self.nimbus, colour)), "Colour {} is out-of-range for this screen mode".format(colour)

        self.nimbus.pen_colour = colour


    def set_charset(self, charset):
        """Set the charset for text

        Args:
            charset (int): 0 is the standard font, 1 is the other font!

        """

        # validate params
        assert isinstance(charset, int), "The value of charset must be an integer, not {}".format(type(charset))
        assert (charset == 0 or charset == 1), "The value of charset can be either 0 or 1, not {}".format(charset)

        self.nimbus.charset = charset


    def ask_charset(self):
        """Return the current charset for text

        Returns:
            charset (int): 0 is the standard font, 1 is the other font

        """

        return self.nimbus.charset


    def set_curpos(self, cursor_position):
        """Set the cursor position

        Args:
            cursor_position (tuple): The new cursor position (column, row)

        """

        # Validate params
        assert isinstance(cursor_position, tuple), "The value of cursor_position must be a tuple, not {}".format(type(cursor_position))
        assert len(cursor_position) == 2, "The cursor_position tuple must have 2 values, not {}".format(len(cursor_position))
        for i in range(0, 2):
            assert isinstance(cursor_position[i], int), "This value in cursor_position must be an integer, not{}".format(type(cursor_position[i]))
        # Validate that cursor will still be on screen
        assert (colrows_to_xy(self.nimbus.screen_size, (cursor_position[0], 1))[0] < self.nimbus.screen_size[0]), "Column {} is not on the screen".format(cursor_position[0])
        assert (colrows_to_xy(self.nimbus.screen_size, (1, cursor_position[1]))[1] >= 0), "Row {} is not on the screen".format(cursor_position[1])
        assert (cursor_position[0] >= 0), "Negative column value in {} is not permitted".format(cursor_position)
        assert (cursor_position[1] >= 0), "Negative row value in {} is not permitted".format(cursor_position)       

        # Now update the cursor position
        self.nimbus.update_cursor_position(cursor_position)


    def ask_curpos(self):
        """Gets the current cursor position

        Returns:
            cursor_position (tuple): The current cursor position (column, row)

        """

        # Return cursor position
        return self.nimbus.get_cursor_position()


    def plot(self, text, coord, size=1, brush=None, direction=0, font=None):
        """Plot text on the screen

        Args:
            text (str): The text to be plotted
            coord (tuple): The (x, y) position of the text
            size (int), optional: Font size. To elongate pass a tuple (x_size, y_size)
            brush (int), optional: Brush colour
            direction (int), optional: 0=normal, 1=-90deg, 2=180deg, 3=-270deg
            font (int), optional: 0 is the standard font, 1 is the other font

        """

        # Validate params
        assert isinstance(text, str), "The value of text must be a string, not {}".format(type(str))
        assert isinstance(coord, tuple), "The value of coord must be a tuple, not {}".format(type(coord))
        assert len(coord) == 2, "The coord tuple must have 2 values, not {}".format(len(coord))
        for i in range(0, 2):
            assert isinstance(coord[i], int), "The values in coord {} must be integer, not {}".format(coord, type(coords[i]))      
        assert isinstance(size, (int, tuple)), "The value of size must be an integer or tuple, not {}".format(type(size))
        if isinstance(size, tuple):
            for i in range(0, 2):
                assert isinstance(size[i], int), "The values in size {} must be integer, not {}".format(size, type(size[i]))  
        assert isinstance(brush, (type(None), int)), "The value of brush must be None or an integer, not {}".format(type(brush))
        assert (brush == is_valid_colour(self.nimbus, brush)), "Brush colour {} is out-of-range for this screen mode".format(brush)
        assert isinstance(direction, int), "The value of direction must be an integer, not {}".format(type(direction))
        assert isinstance(font, (type(None), int)), "The value of font must be an integer, not {}".format(type(font))
        assert (font == 0 or font == 1 or font is None), "The value of font can be 0 or 1, not {}".format(font)
        

        # Handle is_black workaround
        if colour_to_bgr(self.nimbus, brush) == [0, 0, 0]:
            is_black = True
        else:
            is_black = False

        # Handle brush colour
        if brush is None:
            brush = self.nimbus.brush_colour

        # Handle font
        if font is None:
            font = self.nimbus.plot_font

        # Create a temporary image of the plotted text
        plot_img_width = len(text) * 9
        plot_img = np.zeros((10, plot_img_width, 3), dtype=np.uint8)
        x = 0
        for char in text:
            if is_black:
                char_img = cv2.bitwise_not(self.nimbus.font_images[font][ord(char)])
            else:
                char_img = colour_char(self.nimbus, brush, cv2.bitwise_not(self.nimbus.font_images[font][ord(char)]))
            plot_img = plonk_image(self.nimbus, plot_img, char_img, (x, 0), custom_size=(plot_img_width, 10))
            x += 8
        
        # resize
        if isinstance(size, tuple):
            # tuple: extract x_size, y_size
            x_size, y_size = size
        else:
            x_size = size
            y_size = size
        resized = cv2.resize(plot_img, (plot_img.shape[1]*x_size, plot_img.shape[0]*y_size), interpolation=0)
        
        # rotate
        for i in range(0, direction):
            resized = cv2.rotate(resized, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        # rebuild screen and done
        screen_data = self.nimbus.get_screen()
        screen_data = plonk_transparent_image(self.nimbus, screen_data, resized, coord, is_black=is_black)
        self.nimbus.update_screen(screen_data)


    def flush(self):
        """Clears the keyboard buffer

        """

        self.nimbus.keyboard_buffer = []
    

    def gets(self):
        """Get the oldest char in the keyboard buffer

        Equivalent to GET$ in RM Basic

        Returns:
            (str): The oldest char in the buffer
        
        """

        # If the buffer isn't empty pop the last char
        # and return it, otherwise return empty str
        if len(self.nimbus.keyboard_buffer) > 0:
            return self.nimbus.keyboard_buffer.pop(0)
        else:
            return ''


    def input(self, prompt):
        """Collects keyboard input until user presses ENTER

        Args:
            prompt (str): Message to be printed

        Returns:
            (str): The user's response
        
        """
        
        # Validata params
        assert isinstance(prompt, str), "The value of prompt must be a string, not {}".format(type(prompt))

        # Get max columns for this screen mode
        if self.nimbus.screen_size == (320, 250):
            max_columns = 40
        if self.nimbus.screen_size == (640, 250):
            max_columns = 80
        # Flush buffer, reset enter + delete flag
        self.flush()
        self.nimbus.enter_was_pressed = False
        self.nimbus.backspace_was_pressed = False
        # Print the prompt and get start cursor position
        self.put(prompt)
        # Collect response in this string:
        response = ''
        # Collect and echo chars from buffer until enter was pressed
        while not self.nimbus.enter_was_pressed:
            new_char = self.gets()
            response += new_char
            self.put(new_char)
            # Handle delete
            if self.nimbus.backspace_was_pressed and len(response) == 0:
                self.nimbus.backspace_was_pressed = False
            if self.nimbus.backspace_was_pressed and len(response) > 0:
                now_col, now_row = self.ask_curpos()
                response = response[:-1]
                # Move cursor left
                # If we're about to move off the left-hand side of the screen
                # it must be because we're on a line below where the input
                # started.  So, we need to move up one row and locate cursor
                # at right-hand side, wipe whatever char is there, then re-
                # position
                next_col = now_col - 1
                if next_col == 0:
                    # Go up one row
                    next_col = max_columns
                    next_row = now_row - 1
                else:
                    # Go back one column
                    next_row = now_row
                # Wipe char in this location, reposition, and reset flag
                self.set_curpos((next_col, next_row))
                self.put(' ')
                self.set_curpos((next_col, next_row))
                self.nimbus.backspace_was_pressed = False
        # Enter was pressed, flush buffer and reset enter flag
        self.nimbus.enter_was_pressed = False
        self.flush()
        # Force carriage return by smashing the cursor off the screen
        col, row = self.ask_curpos()
        self.nimbus.cursor_position = (255, row)
        self.put('X')
        # Return string
        return response


    def put(self, ascii_data):
        """Put a single character or string at the current cursor position

        Args:
            ascii_data (int/str): If an int is passed the corresponding ASCII character
                                    will be plotted.  If a string is passed then the 
                                    string will be printed without a terminating carriage
                                    return.

        """
        
        # Validate params
        assert isinstance(ascii_data, (str, int)), "The value of ascii_data must be an integer or string, not {}".format(type(ascii_data))

        # Handle is_black workaround
        if colour_to_bgr(self.nimbus, self.nimbus.pen_colour) == [0, 0, 0]:
            is_black = True
        else:
            is_black = False

        # Handle integer
        if isinstance(ascii_data, int):
            # validate in extended ASCII range
            assert (ascii_data >= 0 and ascii_data <= 255), "The value {} of ascii_data is outside the range of Extended ASCII (0-255)".format(ascii_data)
            # convert to char
            ascii_list = [chr(ascii_data)]
        # Handle string
        if isinstance(ascii_data, str):
            ascii_list = ascii_data
        
        # Put char or chars
        for ascii in ascii_list:
            # Get char img
            char_img = self.nimbus.font_images[self.nimbus.charset][ord(ascii)]
            # Get screen position in pixels from cursor position
            curpos_xy = colrows_to_xy(self.nimbus.screen_size, self.nimbus.get_cursor_position())
            # Plot char and apply paper colour underneath char
            screen_data = self.nimbus.get_screen()
            # Paper colour
            cv2.rectangle(
                screen_data, 
                fix_coord(self.nimbus.screen_size, (curpos_xy[0], curpos_xy[1])), 
                fix_coord(self.nimbus.screen_size, (curpos_xy[0] + 8, curpos_xy[1] + 10)), 
                colour_to_bgr(self.nimbus, self.nimbus.paper_colour), 
                -1
            )
            # Overlay char, colourise and preserve paper colour
            if is_black:
                char_img = cv2.bitwise_not(char_img)
            else:
                char_img = colour_char(self.nimbus, self.nimbus.pen_colour, cv2.bitwise_not(char_img))
            screen_data = plonk_transparent_image(self.nimbus, screen_data, char_img, (curpos_xy[0], curpos_xy[1]), is_black=is_black)
            # calculate new curpos, if over the right-hand side do carriage return
            self.nimbus.update_screen(screen_data)
            new_column = self.nimbus.get_cursor_position()[0] + 1
            if colrows_to_xy(self.nimbus.screen_size, (new_column, 1))[0] >= self.nimbus.screen_size[0]:
                # do carriage return
                new_column = 1  # return to left-hand side
                new_row = self.nimbus.get_cursor_position()[1] + 1  # move down
                # if we're below, then screen, move screen data up 10 pixels and set
                # cursor to bottom of screen
                if colrows_to_xy(self.nimbus.screen_size, (1, new_row))[1] < 0:
                    new_row = self.nimbus.get_cursor_position()[1]
                    # Shove screen up.  First crop the top line:
                    old_screen_data = self.nimbus.get_screen()[10:, :]
                    # Make a blank screen and apply paper colour (same as Nimbus did it)
                    screen_data = np.zeros((self.nimbus.screen_size[1]+1, self.nimbus.screen_size[0]+1, 3), dtype=np.uint8)
                    cv2.rectangle(screen_data, (0,0), (self.nimbus.screen_size[0], self.nimbus.screen_size[1]), colour_to_bgr(self.nimbus, self.nimbus.paper_colour),-1)
                    # And overlay the old_screen_data
                    screen_data[:-10, :] = old_screen_data
                    # Update screen
                    self.nimbus.update_screen(screen_data)
            else:
                # don't move cursor down
                new_row = self.nimbus.get_cursor_position()[1]
            # move cursor
            self.set_curpos((new_column, new_row))
         
            
    def print(self, text):
        """Print a string with carriage return at end

        Args:
            text (str): The text to be printed

        """

        # Validate params
        assert isinstance(text, str), "The value of text must be a string, not {}".format(type(text))

        # Put the string and then maybe CR
        self.put(text)
        # Carriage return?
        col, row = self.ask_curpos()
        if col > 1:
            # Yep - smash the cursor off the screen and use put to force CR
            self.nimbus.cursor_position = (255, row)
            self.put('X')


    def line(self, coord_list, brush=None):
        """Draw one or more connected straight lines

        Args:
            coord_list (list): A list of (x, y) tuples
            brush (int), optional: Colour value (High-resolution: 0-3, low-resolution: 0-15)

        """

        # validate params
        assert isinstance(coord_list, list), "coord_list should contain a list, not {}".format(type(coord_list))
        assert isinstance(brush, (type(None), int)), "The value of brush must be None or an integer, not {}".format(type(brush))
        assert (brush == is_valid_colour(self.nimbus, brush)), "Brush colour {} is out-of-range for this screen mode".format(brush)
        for coord in coord_list:
            assert len(coord) == 2, "The coord tuple must have 2 values, not {}".format(len(coord))
            for i in range(0, 2):
                assert isinstance(coord[i], int), "The values in coord {} must be integer, not {}".format(coord, type(coord[i])) 

        # if default brush value then get current brush colour
        if brush is None:
            brush = self.nimbus.brush_colour
        # validate brush
        brush = is_valid_colour(self.nimbus, brush)
        # draw lines on screen
        screen_data = self.nimbus.get_screen()
        for i in range(0, len(coord_list) - 1):
            cv2.line(screen_data, fix_coord(self.nimbus.screen_size, coord_list[i]), fix_coord(self.nimbus.screen_size, coord_list[i+1]), colour_to_bgr(self.nimbus, brush), 1)
        self.nimbus.update_screen(screen_data)
    

    def area(self, coord_list, brush=None):
        """Draw a filled polygon

        Args:
            coord_list (list): A list of (x, y) tuples
            brush (int), optional: Colour value (High-resolution: 0-3, low-resolution: 0-15)

        """

        # validate params
        assert isinstance(coord_list, list), "coord_list should contain a list, not {}".format(type(coord_list))
        assert isinstance(brush, (type(None), int)), "The value of brush must be None or an integer, not {}".format(type(brush))
        assert (brush == is_valid_colour(self.nimbus, brush)), "Brush colour {} is out-of-range for this screen mode".format(brush)
        for coord in coord_list:
            assert len(coord) == 2, "The coord tuple must have 2 values, not {}".format(len(coord))
            for i in range(0, 2):
                assert isinstance(coord[i], int), "The values in coord {} must be integer, not {}".format(coord, type(coord[i]))

        # if default brush value then get current brush colour
        if brush is None:
            brush = self.nimbus.brush_colour
        # validate brush
        brush = is_valid_colour(self.nimbus, brush)
        # convert coord_list into array
        poly_list = []
        for coord in coord_list:
            coord = fix_coord(self.nimbus.screen_size, coord)
            poly_list.append([coord[0], coord[1]])
        # draw filled polygon on screen
        screen_data = self.nimbus.get_screen()
        cv2.fillPoly(screen_data, np.array([poly_list]), colour_to_bgr(self.nimbus, brush))
        self.nimbus.update_screen(screen_data)