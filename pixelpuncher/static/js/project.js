/* Project specific Javascript goes here. */


function increase(id)
{
    var value = parseInt(document.getElementById(id).value, 10);
    value = isNaN(value) ? 0 : value;
    available_points = document.getElementById("id_attribute_points").value;

    if (available_points > 0) {
        value++;
        available_points--;

        document.getElementById('id_attribute_points').value = available_points;
    }

    document.getElementById(id).value = value;
}


function decrease(id, min)
{
    var value = parseInt(document.getElementById(id).value, 10);
    value = isNaN(value) ? 0 : value;
    value--;

    available_points = document.getElementById("id_attribute_points").value;

    if (value < min) {
        value = min;
    }
    else {
        available_points++;
        document.getElementById('id_attribute_points').value = available_points;
    }

    document.getElementById(id).value = value;
}
