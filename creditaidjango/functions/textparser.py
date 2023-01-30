# this is lukas' attempt to parse raw text into correct ktp information form

def lukasextract(raw_text):
    data = raw_text.split(" ")
    data = array_prettier(data)
    return data


def array_prettier(input_array):
    final_string = ""

    final_string = final_string + " \n"

    counter = 1
    for item in input_array:
        final_string = final_string + str(counter) + " " + item + "\n"
        counter += 1

    final_string = final_string + " \n"

    return final_string


def provinsi_parser(raw_input):
    return 0
