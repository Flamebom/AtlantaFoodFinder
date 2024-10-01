document.addEventListener("DOMContentLoaded", function () {
    const folderList = [{ name: 'Favorite', deletable: false }, { name: 'Folder 1', deletable: true }];
    const folderContainer = document.querySelector('.selection-card');
    const createFolderInput = document.querySelector('.new-folder-input');

    // Function to render the folders
    function renderFolders() {
        // Remove all current folder items except for the favorite and create new folder input
        document.querySelectorAll('.folder-item').forEach(item => item.remove());

        folderList.forEach(folder => {
            if (folder.deletable) {
                const folderItem = document.createElement('div');
                folderItem.classList.add('folder-item');
                folderItem.setAttribute('data-folder', folder.name);

                folderItem.innerHTML = `
                    <div class="div">
                        <div class="text-wrapper">${folder.name}</div>
                        <div class="type-2 delete-folder">Delete</div>
                        <img class="img" src="img/generalline-2.svg" />
                        <img class="sky-blue" src="img/sky-blue.svg" />
                    </div>
                `;

                // Add delete functionality
                folderItem.querySelector('.delete-folder').addEventListener('click', function () {
                    const folderName = folderItem.getAttribute('data-folder');
                    deleteFolder(folderName);
                });

                // Insert before the create folder section
                folderContainer.insertBefore(folderItem, document.querySelector('.create-folder-section'));
            }
        });
    }

    // Function to add a new folder
    function addFolder(name) {
        folderList.push({ name, deletable: true });
        renderFolders();
    }

    // Function to delete a folder
    function deleteFolder(name) {
        const index = folderList.findIndex(folder => folder.name === name);
        if (index !== -1) {
            folderList.splice(index, 1);
            renderFolders();
        }
    }

    // Event listener to handle new folder creation on Enter key
    createFolderInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && createFolderInput.value.trim() !== '') {
            addFolder(createFolderInput.value.trim());
            createFolderInput.value = '';  // Clear the input
        }
    });

    // Initial render
    renderFolders();
});
