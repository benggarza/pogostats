function generate_columns(columns) {
    columns_json = []
    for (let i in columns){
        columns_json.push({data: columns[i]});
    }
    return columns_json;
    } 