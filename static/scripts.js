const tabs = document.querySelectorAll('[data-tab-target]')
const tabContents = document.querySelectorAll('[data-tab-content]')

tabs.forEach(tab => {
    tab.addEventListener('click', () =>{
        const target = document.querySelector(tab.dataset.tabTarget)
        tabContents.forEach(tabContent =>{
            tabContent.classList.remove('active')
        })
        tabs.forEach(tab =>{
            tab.classList.remove('active')
        })
        tab.classList.add('active')
        target.classList.add('active')
    })
})

function addCourse() {
    var container = document.getElementById("courseList");
    var template = document.getElementById("courseTemplate");
    var newCourse = document.createElement("course_" + container.children.length)
    newCourse.innerHTML = template.innerHTML.replace(/{i}/g, container.children.length);
    container.append(newCourse);
}

function removeCourse(index) {
    var container = document.getElementById("courseList");
    container.children[index].innerHTML = "";
}