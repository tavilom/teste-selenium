document.addEventListener('DOMContentLoaded', () => {
    const newTaskInput = document.getElementById('new-task');
    const addTaskButton = document.getElementById('add-task');
    const taskList = document.getElementById('task-list');

    addTaskButton.addEventListener('click', addTask);
    newTaskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTask();
        }
    });

    function addTask() {
        const taskText = newTaskInput.value.trim();
        if (taskText !== '') {
            const li = createTaskElement(taskText);
            taskList.appendChild(li);
            newTaskInput.value = '';
            newTaskInput.focus();
        }
    }

    function createTaskElement(taskText) {
        const li = document.createElement('li');
        li.dataset.taskId = taskText;
        const span = document.createElement('span');
        span.textContent = taskText;

        const buttonContainer = document.createElement('div');
        buttonContainer.classList.add('buttons');

        const checkButton = document.createElement('button');
        checkButton.textContent = 'Checar';
        checkButton.classList.add('check-btn');
        checkButton.addEventListener('click', () => toggleTaskCompletion(span));

        const editButton = document.createElement('button');
        editButton.textContent = 'Editar';
        editButton.classList.add('edit-btn');
        editButton.addEventListener('click', () => editTask(li, span));

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Excluir';
        deleteButton.classList.add('delete-btn');
        deleteButton.addEventListener('click', () => {
            taskList.removeChild(li);
        });

        buttonContainer.appendChild(checkButton);
        buttonContainer.appendChild(editButton);
        buttonContainer.appendChild(deleteButton);

        li.appendChild(span);
        li.appendChild(buttonContainer);

        return li;
    }

    function toggleTaskCompletion(span) {
        span.classList.toggle('completed');
    }

    function editTask(li, span) {
        const input = document.createElement('input');
        input.type = 'text';
        input.value = span.textContent;
        li.insertBefore(input, span);
        li.removeChild(span);
        input.focus();

        input.addEventListener('blur', () => {
            span.textContent = input.value;
            li.insertBefore(span, input);
            li.removeChild(input);
        });

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                span.textContent = input.value;
                li.insertBefore(span, input);
                li.removeChild(input);
            }
        });
    }
});
