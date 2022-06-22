function selectElement() {
    if (document.querySelector('#main').addEventListener) {
        document.querySelector('#main').addEventListener("click", selectFromMain);
        document.querySelector('#main').addEventListener("mouseover", makeMainSelectable);
        document.querySelector('#main').addEventListener("mouseout", makeMainSelectable);
    }
}

function selectFromMain(evt) {
    var targetElement = evt.target || evt.srcElement;
    editStyles(targetElement);
    targetElement.style.opacity = 1;
    document.querySelector('#main').removeEventListener("click", makeMainSelectable);
    document.querySelector('#main').removeEventListener("mouseover", makeMainSelectable);
    document.querySelector('#main').removeEventListener("mouseout", makeMainSelectable);
    document.querySelectorAll('.elTag').forEach(el => {
        el.remove();
    });
}

function makeMainSelectable(evt) {
    var targetElement = evt.target || evt.srcElement;

    if (evt.type === "mouseover") {
        targetElement.style.opacity = 0.6;
        document.body.appendChild(generateTag(targetElement));
    } else if (evt.type === "mouseout") {
        targetElement.style.opacity = 1;
        document.querySelectorAll('.elTag').forEach(el => {
            el.remove();
        });
    }
}

const generateTag = target => {
    let text = `${target.tagName.toLowerCase()}`
    if (target.id) {
        text += `#${target.id}`;
    }
    target.classList.forEach(cls => {
        text += `.${cls}`;
    })

    let tag = document.createElement('div');
    tag.classList.add('elTag');
    tag.innerText = text;
    tag.style.right = `${window.innerWidth - (target.offsetLeft + target.offsetWidth)}px`;
    tag.style.top = `${target.offsetTop}px`;

    return tag;
}

function editStyles(el) {
    const rules = document.styleSheets[0].cssRules;
    console.log(rules);
    const selectors = [];

    Object.keys(document.styleSheets[0].cssRules).forEach(rule => {
        selectors.push(rules[rule].selectorText);
    });
    console.log(selectors);

    var sheet = '';

    if (el.id) {
        selectors.forEach(s => {
            if (s === `#${el.id}`) {
                sheet += rules[selectors.indexOf(s)].cssText;
            };
        })
    }

    let matchedStyles = Array.from(el.classList).filter(cls => selectors.includes(`.${cls}`));
    matchedStyles.forEach(cls => {
        sheet += rules[selectors.indexOf(`.${cls}`)].cssText;
    })

    sheet = sheet.replaceAll('{ ', '{\n');
    sheet = sheet.replaceAll('; ', ';\n');
    sheet = sheet.replaceAll('}', '}\n\n')
    document.querySelector('#editor').value = sheet;
}