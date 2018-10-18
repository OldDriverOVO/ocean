function check_file_name_img(file_name) {
    var suffixIndex=file_name.lastIndexOf(".");
    var suffix=file_name.substring(suffixIndex+1).toUpperCase();
    return(suffix!="BMP"&&suffix!="JPG"&&suffix!="JPEG"&&suffix!="PNG"&&suffix!="GIF");

}