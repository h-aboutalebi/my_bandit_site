

// This function is triggered when the user click the save icon
// It saves the reward tensor as a txt file
function save_reward_tensor() {
    var a = document.createElement("a");
    var initial_information_parser = generate_initial_information_parser()
    var reward_tensor = response["reward_tensor"]
    var file = new Blob([initial_information_parser, reward_tensor], {type: 'text/plain'});
    a.href = URL.createObjectURL(file);
    a.download = 'reward_environment.txt';
    a.click()
}


//This function provides the initial string to be used in parser for croping corresponding rewards matrices
function generate_initial_information_parser() {
    var number_of_steps = response['number_of_steps'] + ","
    var number_of_arms = response['number_of_arms'] + ","
    var number_of_iterations = response["number_of_iterations"] + ","
    var bernouli_distribution_arms=response["bernouli_distribution_arms"]+","
    return number_of_iterations + number_of_arms + number_of_steps+bernouli_distribution_arms
}



function process_uploaded_reward_tensor() {
    var fileInput = $('#inputGroupFile04');
    if (!window.FileReader) {
        alert('Your browser is not supported');
        return false;
    }
    var input = fileInput.get(0);

    // Create a reader object
    var reader = new FileReader();
    if (input.files.length) {
        var textFile = input.files[0];
        // Read the file
        reader.readAsText(textFile);
        // When it's loaded, process it
        $(reader).on('load', processFile);
    } else {
        alert('Please upload a file before continuing')
    }
}

function processFile(e) {
    var file = e.target.result,
        results;
    if (file && file.length) {
        results = file.split("\n");
        uploaded_reward_tensor=results
        document.getElementById("reward_tensor").value=results
    }
}