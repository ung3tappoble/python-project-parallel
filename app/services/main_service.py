from database.data import read_query, insert_query

def get_latest_mouse_data():
    mouse_data = read_query('SELECT x_coordinate, y_coordinate FROM MouseData ORDER BY timestamp DESC LIMIT 1')
    image_data = read_query('SELECT image FROM ImageData ORDER BY timestamp DESC LIMIT 1')

    if mouse_data and image_data:
        x_coordinate, y_coordinate = mouse_data[0]
        image = image_data[0][0] 
        return x_coordinate, y_coordinate, image
    else:
        return None
   

def save_mouse_data(x_coordinate, y_coordinate, image_data):
    mouse_data_id = insert_query('INSERT INTO MouseData (x_coordinate, y_coordinate) VALUES (?,?)',
                                 (x_coordinate, y_coordinate))

    insert_query('INSERT INTO ImageData (mouse_data_id, image) VALUES (?,?)',
                 (mouse_data_id, image_data))
    