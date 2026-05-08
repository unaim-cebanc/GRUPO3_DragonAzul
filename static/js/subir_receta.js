function añadirIngrediente() {
    var body = document.getElementById("container_ingrediente");
    var div = document.createElement('div');
    div.innerHTML = `
        <input type="text" name="ingredientes[]" id="ingredeintes" required>
            <label for="cantidad">Cantidad:</label>
            <input type="number" name="cantidad[]" id="cantidad" min="0" max="999">
            <label for="unidad">Unidad:</label>
            <select name="unidad[]" id="unidad">
                <option value="mg">mg</option>
                <option value="g">g</option>
                <option value="ml">ml</option>
                <option value="l">l</option>
                <option value="cda.">cda.</option>
                <option value="cdta.">cdta.</option>
                <option value="none" selected></option>
            </select>`;
    body.appendChild(div);
}

function añadirPaso() {
    var body = document.getElementById("container_paso");
    var textarea = document.createElement('textarea');
    textarea.name = 'pasos[]';
    textarea.placeholder = 'Introduce el paso';
    textarea.required = true;
    body.appendChild(textarea);
}