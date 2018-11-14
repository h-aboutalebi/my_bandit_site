//This is ajax response
var response
var list_Algorithms_name
var x_range
var x_list
var number_of_arms
var uploaded_reward_tensor=""




//This function uses ajax to send the submitted to form to the server
function send_form_to_server() {
    var my_form = $("form")
    activate_loading()
    $.ajax({
        type: 'POST',
        url: "handle_sim_ncontinous_env_ajax/",
        data: my_form.serialize(),
        dataType: 'json',
        success: function (data) {
            $('#figure_results').empty()
            response = data
            list_Algorithms_name = data["list_Algorithms_name"]
            x_range = data["number_of_steps"]
            x_list = data['x_list']
            number_of_arms = data["number_of_arms"]
            draw_figure(data)
            deactivate_loading()
            window.location.hash = '#figure_results';
        }
    });
    
}

//This function shows loading icon after pressing submit
function activate_loading() {
    $('.not_loading').css('display','none')
    $('.loading').css('display','block')
}

//This function hides loading icon
function deactivate_loading() {
    $('.not_loading').css('display','')
    $('.loading').css('display','none')
}

function draw_figure(data) {
    reset_form_input_reward_tensor()
    draw_regret_graph(data)
    draw_accumulated_regret_graph(data)
    draw_accumulated_reward_graph(data)
    draw_optimal_arm_percentage_graph(data)
    draw_worst_arm_percentage_graph(data)
    var algorithm_number = 0
    for (algorithm_number = 0; algorithm_number < list_Algorithms_name.length; algorithm_number++) {
        draw_arm_selection_history_all_algorithm(data, algorithm_number)
        draw_arm_confidence_all_algorithm(data, algorithm_number)
    }
    
}

//This function draw figure corresponding to arm selection history of a given algorithm number
function draw_arm_selection_history_all_algorithm(data, algorithm_number) {
    var title = "Arm Play History of Algorithm " + list_Algorithms_name[algorithm_number]
    var y_title = "Percentage"
    var String_title = [title, y_title]
    var canvas_div = create_canvas_div()
    var arm_number = 0
    var lines = []
    for (arm_number = 0; arm_number < number_of_arms; arm_number++) {
        // debugger;
        var mean = data["arm_selection_history_all_algorithm_list"][algorithm_number][0][arm_number]
        var std = data["arm_selection_history_all_algorithm_list"][algorithm_number][1][arm_number]
        var input_data = {'String_title': String_title, 'mean': [mean], 'std': [std], 'label': arm_number + 1, 'i': 0}
        var upper_bound = set_upper_bound_line_ROA(input_data, arm_number + 1)
        var trace = set_mean_trace_line_ROA(input_data, arm_number + 1)
        var lower_bound = set_lower_bound_line_ROA(input_data, arm_number + 1)
        lines.push(lower_bound)
        lines.push(trace)
        lines.push(upper_bound)
    }
    var layout = set_layeout_figure(String_title)
    // Plotly.plot(canvas_div, lines,layout)
    Plotly.plot(canvas_div, lines, layout)
}

//This function draw figure corresponding to arm selection history of a given algorithm number
function draw_arm_confidence_all_algorithm(data, algorithm_number) {
    var title = "Confidence interval of arms for Algorithm " + list_Algorithms_name[algorithm_number]
    var y_title = "amount "
    var String_title = [title, y_title]
    var canvas_div = create_canvas_div()
    var arm_number = 0
    var lines = []
    for (arm_number = 0; arm_number < number_of_arms; arm_number++) {
        // debugger;
        var mean = data["arm_confidence_all_algorithm_list"][algorithm_number][0][arm_number]
        var std = data["arm_confidence_all_algorithm_list"][algorithm_number][1][arm_number]
        var input_data = {'String_title': String_title, 'mean': [mean], 'std': [std], 'label': arm_number + 1, 'i': 0}
        var upper_bound = set_upper_bound_line_ROA(input_data, arm_number + 1)
        var trace = set_mean_trace_line_ROA(input_data, arm_number + 1)
        var lower_bound = set_lower_bound_line_ROA(input_data, arm_number + 1)
        lines.push(lower_bound)
        lines.push(trace)
        lines.push(upper_bound)
    }
    var layout = set_layeout_figure(String_title)
    // Plotly.plot(canvas_div, lines,layout)
    Plotly.plot(canvas_div, lines, layout)
}



//This function draw figure corresponding to optimal arm play percentage
function draw_optimal_arm_percentage_graph(data) {
    var title = "Percentage of Optimal Arm Play"
    var y_title = "Percentage"
    var String_title = [title, y_title]
    var mean = data["optimal_arm_percentage"][0]
    var std = data["optimal_arm_percentage"][1]
    var input_data = {'String_title': String_title, 'mean': mean, 'std': std}
    draw_ROA(input_data)
}

//This function draw figure corresponding to worst arm play percentage
function draw_worst_arm_percentage_graph(data) {
    var title = "Percentage of Worst Arm Play"
    var y_title = "Percentage"
    var String_title = [title, y_title]
    var mean = data["worst_arm_percentage"][0]
    var std = data["worst_arm_percentage"][1]
    var input_data = {'String_title': String_title, 'mean': mean, 'std': std}
    draw_ROA(input_data)
}


//This function draw figure corresponding to cumulative reward
function draw_accumulated_reward_graph(data) {
    var title = "Total Accumulated Reward"
    var y_title = "Accumulated Reward"
    var String_title = [title, y_title]
    var mean = data["cumulative_reward"][0]
    var std = data["cumulative_reward"][1]
    var input_data = {'String_title': String_title, 'mean': mean, 'std': std}
    draw_ROA(input_data)
}

//This function draw figure corresponding to regret
function draw_regret_graph(data) {
    var title = "Expected Regret per step"
    var y_title = "Expected Regret"
    var String_title = [title, y_title]
    var mean = data["regret_figure"][0]
    var std = data["regret_figure"][1]
    var input_data = {'String_title': String_title, 'mean': mean, 'std': std}
    draw_ROA(input_data)
}

//This function draw figure corresponding to accumulated regret
function draw_accumulated_regret_graph(data) {
    var title = "Accumulated Regret per step"
    var y_title = "Accumulated Regret"
    var String_title = [title, y_title]
    var mean = data["accumulated_regret"][0]
    var std = data["accumulated_regret"][1]
    var input_data = {'String_title': String_title, 'mean': mean, 'std': std}
    draw_ROA(input_data)
}


//This function will draw the  figures corresponding to Regret, Optimal action percebtage, Accumulated rewards
function draw_ROA(input_data) {
    var canvas_div = create_canvas_div()
    var i = 0
    var lines = []
    for (i = 0; i < list_Algorithms_name.length; i++) {
        input_data['i'] = i
        input_data['label'] = list_Algorithms_name[i]
        var upper_bound = set_upper_bound_line_ROA(input_data)
        var trace = set_mean_trace_line_ROA(input_data)
        var lower_bound = set_lower_bound_line_ROA(input_data)
        lines.push(lower_bound)
        lines.push(trace)
        lines.push(upper_bound)
    }
    var layout = set_layeout_figure(input_data['String_title'])
    // Plotly.plot(canvas_div, lines,layout)
    Plotly.plot(canvas_div, lines, layout)
    
}

//sets the layout for regret figure
function set_layeout_figure(String_title) {
    var layout = {
        yaxis: {title: String_title[1]},
        xaxis: {title: 'number of steps'},
        width: 1000,
        height: 500,
        title: String_title[0],
        showlegend: true
    }
    return layout
}

//This function sets the uppererror of a line
function set_upper_bound_line_ROA(input_data, arm_number) {
    var i = input_data['i']
    if (arm_number == undefined) {
        arm_number = i
    }
    var upper_bound = {
        name: 'UBound ' + input_data['label'],
        x: x_list,
        showlegend: false,
        y: add_arrays(input_data['mean'][i], input_data['std'][i]),
        fill: "tonexty",
        fillcolor: opacity_version_rgba(my_color_map[arm_number]),
        type: "scatter",
        mode: 'none'
    }
    return upper_bound
}

//This function sets the uppererror of a line
function set_mean_trace_line_ROA(input_data, arm_number) {
    var i = input_data['i']
    if (arm_number == undefined) {
        arm_number = i
    }
    var mean_trace = {
        name: 'mean ' + input_data['label'],
        x: x_list,
        y: input_data['mean'][i],
        fill: "tonexty",
        marker: {color: my_color_map[arm_number]},
        mode: "lines",
        type: "scatter"
    };
    return mean_trace
}


//This function sets the lowererror of a line
function set_lower_bound_line_ROA(input_data, arm_number) {
    var i = input_data['i']
    if (arm_number == undefined) {
        arm_number = i
    }
    var lower_bound = {
        name: 'LBound' + input_data['label'],
        x: x_list,
        showlegend: false,
        y: subtract_arrays(input_data['mean'][i], input_data['std'][i]),
        line: {color: "transparent"},
        marker: {color: "rgb(66, 134, 244)"},
        mode: "lines",
        type: "scatter"
    }
    return lower_bound
}

//This function subtracts the elements of array_1 from array_2
function subtract_arrays(array_1, array_2) {
    var i = 0
    result = []
    for (i = 0; i <= array_1.length; i++) {
        result.push(array_1[i] - array_2[i] / 3)
    }
    return result
}

//This function add the elements of array_1 from array_2
function add_arrays(array_1, array_2) {
    var i = 0
    result = []
    for (i = 0; i <= array_1.length; i++) {
        result.push(array_1[i] + array_2[i] / 3)
    }
    return result
}

//This function creates the div for corresponding figure inside '#figure_results' div
function create_canvas_div() {
    var mydiv = document.createElement("div")
    mydiv.className += " figure_div  "
    $('#figure_results').append(mydiv)
    return mydiv
}

//This function is for resetting the value of reward tensor input of the form
function reset_form_input_reward_tensor(){
    document.getElementById("reward_tensor").value=""
}