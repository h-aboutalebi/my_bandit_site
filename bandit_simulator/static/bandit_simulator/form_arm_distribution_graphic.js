
//these two global values are for slide bar input figure and corresponding value displayer span
var figure
var displayer
var dropdown_is_selected=false

$(document).ready(function() {
    
    

});


//This code will generate the fields related to each arm to get the correponding distribution from user
function create_arms_distributions_fields(number_of_arms) {
    var i=0
    $("#arm_related_distribution_inputs").empty()
    for(i=0;i<number_of_arms;i++) {
        var div_row=document.createElement("div")
        div_row.setAttribute("class","row")
        div_row.className += " form_arm_slider_div"
        var input_distribution_label=provide_label_arm_distribution(i+1)
        var slide_bar_figure=create_slide_bar_figure(i+1)
        var slide_bar_range_value_displayer=create_slide_bar_range_value_displayer(i+1)
        effect(figure,displayer)
        div_row.append(input_distribution_label,slide_bar_figure,slide_bar_range_value_displayer)
        $("#arm_related_distribution_inputs").append(div_row)
    }
}

//This function provides the labels corresponding to the distributions of arms. This input is provided by end user
function provide_label_arm_distribution(arm_number){
    var my_div_col=create_div_col_element()
    var my_label=document.createElement("label")
    my_label.className+=" label_arm_distribution"
    my_label.innerHTML="Mean of arm " + arm_number
    $(my_div_col).append(my_label)
    return  my_div_col
}


// This function add graphic inteface of slide bar
function create_slide_bar_figure(arm_number){
    var my_div_field=create_div_col_element()
    var my_label=document.createElement("label")
    my_label.setAttribute("for","range")
    var my_slide_bar_figure=document.createElement("input")
    my_slide_bar_figure.setAttribute("type","range")
    my_slide_bar_figure.setAttribute("name","range")
    var id_slide_bar_figure="id_slide_bar_figure#"+arm_number
    my_slide_bar_figure.setAttribute("id",id_slide_bar_figure)
    my_slide_bar_figure.setAttribute("min","0")
    my_slide_bar_figure.setAttribute("max","1")
    my_slide_bar_figure.setAttribute("step","0.05")
    var random_input=Math.random()
    my_slide_bar_figure.setAttribute("value",random_input)
    figure=my_slide_bar_figure
    $(my_label).append(my_slide_bar_figure)
    $(my_div_field).append(my_label)
    return my_div_field
}

//This function creates the displayer for the range of slidebar figure
function create_slide_bar_range_value_displayer(arm_number) {
    var my_div_field=create_div_col_element()
    var my_slide_bar_range_value_displayer=document.createElement("span")
    my_slide_bar_range_value_displayer.className+=" range-slider__value"
    var id_for_slidebar_range_value="id_slide_bar_range_value_displayer#"+arm_number
    my_slide_bar_range_value_displayer.setAttribute("id",id_for_slidebar_range_value)
    displayer=my_slide_bar_range_value_displayer
    $(my_div_field).append(my_slide_bar_range_value_displayer)
    return my_div_field
}

// This function add effect to each slide bar (changing value effect)
function effect(slide_bar_figure,slide_bar_range_value_displayer){
    // This code is for slide bar effects
    $(slide_bar_figure).on("change", function() {
    $(slide_bar_range_value_displayer).text(this.value  );
    }).trigger("change");
}

function create_div_col_element(){
    var my_div=document.createElement("div")
    my_div.setAttribute("class","col-sm")
    return my_div
}

function chosen_number_of_arms(element){
    dropdown_is_selected=true
    create_arms_distributions_fields($(element).text())
}

