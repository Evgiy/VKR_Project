function showForm() {
    const category =
        document.getElementById('categorySelect').value;
    const form =
        document.getElementById('reviewForm');
    const dynamicFields =
        document.getElementById('dynamicFormFields');
    const template =
        document.getElementById(`${category}-form`);
    const photoBox =
        document.querySelector('.review-photo-box');
    const clearBtn =
        document.getElementById('clearPhotoBtn');
    const publishBtn =
        document.getElementById('publishBtn');
    const hiddenInput =
        document.getElementById('hiddenFileInput');
    const img =
        document.getElementById('previewImage');
    const plus =
        document.getElementById('plusIcon');

    document.querySelectorAll('select[multiple]').forEach(select => {
        if (select.tomselect) {
            select.tomselect.destroy();
        }
    });

    dynamicFields.innerHTML = '';
    img.src = '';
    img.style.display = 'none';
    plus.style.display = 'block';
    hiddenInput.value = '';
    photoBox.style.display = 'none';
    clearBtn.style.display = 'none';
    publishBtn.style.display = 'none';

    if (!category) {
        form.style.display = 'none';
        return;
    }

    if (category === 'restaurant' || category === 'event') {
        hiddenInput.name = 'photo';
    } else {
        hiddenInput.name = 'cover';
    }

    form.style.display = 'block';
    photoBox.style.display = 'flex';
    clearBtn.style.display = 'inline-block';
    publishBtn.style.display = 'inline-block';

    form.action = `/main/create/${category}/`;

    if (template) {
        dynamicFields.innerHTML = template.innerHTML;
    }

    dynamicFields.innerHTML += `
        <p>
            <label>Оценка</label>

            <select name="rating" required>
                <option value="">---</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
            </select>
        </p>

        <p>
            <label>Отзыв</label>

            <textarea name="full_text" rows="4"></textarea>
        </p>
    `;

    initTagSelects();
}

function initTagSelects() {
    document.querySelectorAll('select[multiple]').forEach(select => {
        new TomSelect(select, {
            plugins: ['remove_button'],
            create: false,
            persist: false,
            maxItems: null,
            placeholder: 'Выберите теги...'
        });
    });
}

    function hideAll() {
  const panels = document.querySelectorAll('.panel');
  panels.forEach(panel => panel.style.display = 'none');
}

    function showReview() {
      hideAll();
      document.getElementById('reviewPanel').style.display = 'block';
    }

    function showGrid() {
  hideAll();

  fetch('/main/')
    .then(response => response.text())
    .then(html => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const newGrid = doc.getElementById('gridPanel');

      if (newGrid) {
        const oldGrid = document.getElementById('gridPanel');
        oldGrid.innerHTML = newGrid.innerHTML;
        oldGrid.style.display = 'block';
      }
    })
    .catch(err => console.error('Ошибка при обновлении грида:', err));
}

    function showGrid2() {
      hideAll();
      document.getElementById("grid2").style.display = "grid";
    }

    function showAbout() {
      hideAll();
      document.getElementById('aboutPanel').style.display = 'block';
    }

    function openEditPanel(category, reviewId) {
    const panel = document.getElementById('editPanel');
    const overlay = document.getElementById('editOverlay');

    panel.style.display = 'block';
    overlay.style.display = 'block';

    fetch(`/main/edit_form/${category}/${reviewId}/`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('editRating').value = data.rating || '';
            document.getElementById('editFullText').value = data.full_text || '';

            const form = document.getElementById('editForm');
            form.dataset.reviewId = reviewId;
            form.dataset.category = category;

            form.onsubmit = function(e) {
                e.preventDefault();

                const formData = new FormData(form);

                fetch(`/main/edit/${category}/${reviewId}/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                })
                .then(res => {
                    if (res.ok) {
                        alert('Изменения сохранены!');
                        closeEditPanel();
                        showGrid();
                    } else {
                        alert('Ошибка при сохранении!');
                    }
                })
                .catch(() => {
                    alert('Ошибка соединения!');
                });
            };
        })
        .catch(() => {
            alert('Не удалось загрузить данные отзыва!');
        });
}

function closeEditPanel() {
    document.getElementById('editPanel').style.display = 'none';
    document.getElementById('editOverlay').style.display = 'none';
}

function triggerFileInput() {
    document.getElementById('hiddenFileInput').click();
}

document.getElementById('hiddenFileInput').addEventListener('change', function() {

    const file = this.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const img = document.getElementById('previewImage');
        const plus = document.getElementById('plusIcon');

        img.src = e.target.result;
        img.style.display = 'block';
        plus.style.display = 'none';
    };
    reader.readAsDataURL(file);

    const activeForm = document.querySelector('.add-review-form[style*="block"]');
    if (activeForm) {
        let realFileInput = activeForm.querySelector('input[type="file"]');
        if (realFileInput) {
            realFileInput.files = this.files;
        }
    }
});

document.getElementById('hiddenEditFileInput').addEventListener('change', function() {
    const file = this.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const img = document.getElementById('editPreviewImage');
        const plus = document.getElementById('editPlusIcon');

        img.src = e.target.result;
        img.style.display = 'block';
        plus.style.display = 'none';
    };
    reader.readAsDataURL(file);

    const formInput = document.querySelector('#editForm input[type="file"]');
    if (formInput) {
        formInput.files = this.files;
    }
});

function triggerEditFileInput() {
    document.getElementById('hiddenEditFileInput').click();
}

document.getElementById('hiddenFileInput').addEventListener('change', function() {
    const file = this.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const img = document.getElementById('previewImage');
        const plus = document.getElementById('plusIcon');

        img.src = e.target.result;
        img.style.display = 'block';
        plus.style.display = 'none';
    };
    reader.readAsDataURL(file);

    const realFileInput = document.querySelector('#reviewForm input[type="file"]');
    if (realFileInput) {
        realFileInput.files = this.files;
    }
});

function openReviewsPanel(category, pk) {
    fetch(`/main/reviews/${category}/${pk}/`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('reviewsContent').innerHTML = data.html;
            document.getElementById('reviewsOverlay').style.display = 'block';
            document.getElementById('reviewsPanel').style.display = 'block';
        });
}

function closeReviewsPanel() {
    document.getElementById('reviewsOverlay').style.display = 'none';
    document.getElementById('reviewsPanel').style.display = 'none';
}

function closeReviewsPanel() {
    document.getElementById('reviewsOverlay').style.display = 'none';
    document.getElementById('reviewsPanel').style.display = 'none';
}

      function deleteReview(category, reviewId, formElem) {
    const csrfToken = formElem.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/main/delete/${category}/${reviewId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const card = formElem.closest('.review-card');
            if (card) card.remove();
        } else {
            alert('Ошибка при удалении!');
        }
    })
    .catch(err => {
        console.error(err);
        alert('Ошибка при удалении!');
    });
    return false;
}

      function clearPhoto() {
    const hiddenInput = document.getElementById('hiddenFileInput');
    const preview = document.getElementById('previewImage');
    const plus = document.getElementById('plusIcon');
    const photoBox = document.querySelector('.review-photo-box');
    const clearBtn = document.getElementById('clearPhotoBtn');

    hiddenInput.value = '';

    preview.src = '';
    preview.style.display = 'none';

    plus.style.display = 'block';
}

      function showProfile() {
      hideAll();
    document.getElementById('profilePanel').style.display = 'block';
    document.getElementById('profileOverlay').style.display = 'block';
}

function closeProfilePanel() {
    document.getElementById('profilePanel').style.display = 'none';
    document.getElementById('profileOverlay').style.display = 'none';
}

function filterReviews() {
    const category =
        document.getElementById('categoryFilter').value;
    const dateOrder =
        document.getElementById('dateFilter').value;
    const grid =
        document.getElementById('gridPanel');
    const cards =
        Array.from(grid.querySelectorAll('.review-card'));

    cards.forEach(card => {
        const cardCategory =
            card.dataset.category;
        if (
            category === 'all' ||
            cardCategory === category
        ) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });

    cards.sort((a, b) => {
        const dateA =
            parseInt(a.dataset.date);
        const dateB =
            parseInt(b.dataset.date);
        if (dateOrder === 'new') {
            return dateB - dateA;
        } else {
            return dateA - dateB;
        }
    });

    cards.forEach(card => {
        grid.appendChild(card);
    });
}

function filterRecommendations() {
    const category =
        document.getElementById(
            'recommendationCategoryFilter'
        ).value;

    const cards =
        document.querySelectorAll(
            '#grid2 .review-card'
        );

    cards.forEach(card => {
        const cardCategory =
            card.dataset.category;
        if (
            category === 'all' ||
            category === cardCategory
        ) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}