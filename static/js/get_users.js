const mainBlock = document.querySelector("#main-block");
const friendButton = document.querySelector("#friend-finder");
const access = localStorage.getItem("access");

// создаём блоки динамически
const searchBlock = document.createElement("div");
searchBlock.id = "search-block";
const usersBlock = document.createElement("div");
usersBlock.id = "users-list";

// при первом клике вставим в DOM
function initFriendsUI() {
    if (!mainBlock.contains(searchBlock)) {
        mainBlock.appendChild(searchBlock);
    }
    if (!mainBlock.contains(usersBlock)) {
        mainBlock.appendChild(usersBlock);
    }
}

async function getFriends () {
    try {
        const response = await fetch("/api/v1/users/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access}`
            }
        });

        if (!response.ok) {
            throw new Error(`Ошибка ${response.status}`);
        }

        const apiData = await response.json();
        console.log(apiData);

        usersBlock.innerHTML = apiData.results.map(user => `
            <div class="user-card flex items-center gap-4 p-4 mb-3 bg-white border rounded-xl shadow hover:shadow-md transition" 
            data-user-id="${user.id}">
                <!-- Аватар -->
                <div class="w-12 h-12 rounded-full bg-gray-200 overflow-hidden flex-shrink-0">
                    ${user.avatar 
                        ? `<img src="${user.avatar}" alt="${user.username}" class="w-full h-full object-cover">` 
                        : `<span class="flex items-center justify-center w-full h-full text-gray-500">👤</span>`}
                </div>
                <!-- Инфо -->
                <div>
                    <div class="font-semibold text-gray-800">${user.username}</div>
                    <div class="text-sm text-gray-600">${user.first_name} ${user.last_name}</div>
                </div>
            </div>
        `).join("");

        document.querySelectorAll(".user-card").forEach(card => {
            card.addEventListener("click", async () => {
                const userId = card.dataset.userId;
                console.log("Открываю профиль:", userId);

                try {
                    const response = await fetch(`/api/v1/users/${userId}/`, {
                        headers: {
                            "Authorization": `Bearer ${access}`
                        }
                    });

                    if (!response.ok) {
                        throw new Error(`Ошибка ${response.status}`);
                    }

                    const userData = await response.json();
                    console.log("Детали пользователя:", userData);

                    // тут можешь перерисовать usersBlock под подробный профиль
                    usersBlock.innerHTML = `
                        <div class="p-4 border rounded-xl bg-white shadow">
                            <div class="flex items-center gap-4">
                                <div class="w-20 h-20 rounded-full overflow-hidden bg-gray-200">
                                    ${userData.avatar 
                                        ? `<img src="${userData.avatar}" alt="${userData.username}" class="w-full h-full object-cover">`
                                        : `<span class="flex items-center justify-center w-full h-full h-full text-gray-500">👤</span>`
                                    }
                                </div>
                                <div>
                                    <h2 class="text-xl font-bold">${userData.username}</h2>
                                    <p class="text-gray-600">${userData.first_name} ${userData.last_name}</p>
                                </div>
                            </div>
                            <div class="mt-4">
                                <p class="text-gray-700">Email: ${userData.email ?? "не указан"}</p>
                            </div>
                        </div>
                    `;
                } catch (err) {
                    console.error("Ошибка при получении пользователя:", err);
                }
            });
        });


    } catch (err) {
        console.error("Ошибка при запросе:", err);
        usersBlock.innerHTML = `<p style="color:red;">Не удалось загрузить пользователей</p>`;
    }
}

function renderSearch() {
    searchBlock.innerHTML = `
        <div class="mb-4">
            <input 
                id="search-input"
                type="text" 
                placeholder="Поиск друзей..." 
                class="w-full p-2 border rounded-lg shadow-sm focus:ring focus:ring-blue-300 focus:outline-none"
            >
        </div>
    `;
}

friendButton.addEventListener("click", async (e) => {
    e.preventDefault();
    initFriendsUI();
    renderSearch();
    await getFriends();
});