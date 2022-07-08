function generate_columns(columns) {
    columns_json = []
    for (let column of columns){
        columns_json.push({data: column});
    }
    return columns_json;
    } 