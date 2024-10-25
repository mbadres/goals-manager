document.addEventListener('DOMContentLoaded', function() {
    initializeGoalFilters();
});

function initializeGoalFilters() {
    // Add event listeners to filter elements
    const departmentFilter = document.getElementById('departmentFilter');
    const scoreFilter = document.getElementById('scoreFilter');
    const searchInput = document.getElementById('searchInput');

    if (departmentFilter && scoreFilter && searchInput) {
        departmentFilter.addEventListener('change', filterGoals);
        scoreFilter.addEventListener('change', filterGoals);
        searchInput.addEventListener('input', filterGoals);
    }
}

function filterGoals() {
    const department = document.getElementById('departmentFilter').value;
    const score = document.getElementById('scoreFilter').value;
    const search = document.getElementById('searchInput').value.toLowerCase();

    document.querySelectorAll('.goal-row').forEach(row => {
        const rowDepartment = row.dataset.department;
        const rowScore = parseInt(row.dataset.score);
        const rowText = row.textContent.toLowerCase();

        let showRow = true;

        // Department filter
        if (department && rowDepartment !== department) {
            showRow = false;
        }

        // Score filter
        if (score) {
            if (score === 'high' && rowScore < 8) showRow = false;
            if (score === 'medium' && (rowScore < 4 || rowScore > 7)) showRow = false;
            if (score === 'low' && rowScore > 3) showRow = false;
        }

        // Search filter
        if (search && !rowText.includes(search)) {
            showRow = false;
        }

        row.style.display = showRow ? '' : 'none';
    });
}

function resetFilters() {
    document.getElementById('departmentFilter').value = '';
    document.getElementById('scoreFilter').value = '';
    document.getElementById('searchInput').value = '';
    document.querySelectorAll('.goal-row').forEach(row => {
        row.style.display = '';
    });
}

// Delete functionality
function confirmDelete(goalId) {
    const modal = document.getElementById('deleteModal');
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = `/goals/${goalId}/delete`;
    modal.classList.add('is-active');
}

function closeModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.remove('is-active');
}