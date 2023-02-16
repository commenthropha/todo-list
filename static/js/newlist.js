count = 1;

function newListItem() {
    const newItem = document.createElement("div");
    newItem.className = "field";
    newItem.id = "item " + count;
    const newItemLabel = document.createElement("label");
    newItemLabel.className = "label";
    newItemLabel.for = "listitem" + count
    newItemLabel.textContent = "List Item " + count;
    newItem.appendChild(newItemLabel);
    const controlDiv = document.createElement("div");
    controlDiv.className = "control";
    newItem.appendChild(controlDiv);
    const itemInput = document.createElement("input");
    itemInput.className = "input";
    itemInput.type = "text";
    itemInput.name = "listitem" + count
    itemInput.placeholder = "Enter text here";
    itemInput.required = true;
    controlDiv.appendChild(itemInput);

    const element = document.getElementById("inputs");
    element.appendChild(newItem);
    count++;
    updateCount();
    return false;
}

function removeItem() {
    const element = document.getElementById("item " + (count - 1))
    element.remove();
    count--;
    updateCount();
    return false;
}

function updateCount() {
    const element = document.getElementById("countTracker")
    element.value = count
}