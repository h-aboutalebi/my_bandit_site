var my_color_map = ['rgb(242,121,121)', 'rgb(140,77,35)', 'rgb(153,128,77)', 'rgb(87,102,26)', 'rgb(0,102,54)', 'rgb(0,112,140)', 'rgb(124,146,166)', 'rgb(0,0,242)', 'rgb(143,0,179)', 'rgb(102,0,68)', 'rgb(102,51,65)', 'rgb(229,31,0)', 'rgb(229,161,115)', 'rgb(178,143,0)', 'rgb(152,217,108)', 'rgb(143,191,169)', 'rgb(128,230,255)', 'rgb(26,56,102)', 'rgb(0,0,230)', 'rgb(230,128,255)', 'rgb(217,0,116)', 'rgb(217,163,177)', 'rgb(140,110,105)', 'rgb(217,116,0)', 'rgb(255,251,191)', 'rgb(45,64,32)', 'rgb(57,230,172)', 'rgb(13,38,51)', 'rgb(51,92,204)', 'rgb(29,16,64)', 'rgb(148,77,153)', 'rgb(51,13,33)', 'rgb(102,0,14)', 'rgb(76,48,38)', 'rgb(51,34,0)', 'rgb(218,230,57)', 'rgb(0,255,0)', 'rgb(38,77,74)', 'rgb(64,166,255)', 'rgb(32,45,128)', 'rgb(208,191,255)', 'rgb(255,0,204)', 'rgb(255,0,68)']


//It causes to add opacity feature to a given rgb (needed for ployly continous error bar)
function opacity_version_rgba(rgba_string) {
    var added_string = ",0.5"
    var new_rgba_string = check_it_is_rgba(rgba_string) //this is to make sure the string starts with rgba not rgb
    var position = new_rgba_string.length - 1
    var output = [new_rgba_string.slice(0, position), added_string, new_rgba_string.slice(position)].join('');
    return output
}

//This function is to make sure the string starts with rgba not rgb
function check_it_is_rgba(input_string) {
    var output = input_string
    if (input_string.charAt(3) == '(') {
        var position = 3
        var added_string = 'a'
        output = [input_string.slice(0, position), added_string, input_string.slice(position)].join('');
    }
    return output
}