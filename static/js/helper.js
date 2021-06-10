function reformat(item){
    newItem = ""
    try{
        newItem = item.replaceAll("&#39;", "\"")
    } catch{
        newItem = item
    }
    return newItem

}