// document.addEventListener("DOMContentLoaded", () => {
//   const regBtn = document.getElementById("reg-btn");
//   const regModal = document.getElementById("registerModal");
//   const cancelBtn = document.getElementById("register-cancel");
//   const regForm = document.getElementById("register-form");

//   // открыть модалку
//   regBtn?.addEventListener("click", (e) => {
//     e.preventDefault();
//     regModal.showModal();
//   });

//   // закрыть модалку
//   cancelBtn?.addEventListener("click", (e) => {
//     e.preventDefault();
//     regModal.close();
//   });

//   // сабмит формы
//   regForm?.addEventListener("submit", async (e) => {
//     e.preventDefault();

//     const username = regForm.querySelector("[name='username']").value;
//     const email = regForm.querySelector("[name='email']").value;
//     const password = regForm.querySelector("[name='password']").value;

//     try {
//       const resp = await fetch("/api/v1/registration/", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ username, email, password }),
//       });

//       const data = await resp.json().catch(() => ({}));

//       if (!resp.ok) {
//         alert("Ошибка: " + (data.detail || JSON.stringify(data)));
//         return;
//       }

//       alert("Регистрация успешна! Проверьте почту для активации.");
//       regModal.close();
//     } catch (err) {
//       alert("Ошибка соединения: " + err);
//     }
//   });
// });

document.addEventListener("DOMContentLoaded", () => {
  const regForm = document.getElementById("register-form");
  const regModal = document.getElementById("registerModal");
  const errorBox = document.getElementById("register-error");

  regForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBox.classList.add("hidden");

    const formData = new FormData(regForm);
    const username = formData.get("username");
    const email = formData.get("email");
    const password = formData.get("password");
    const avatarFile = formData.get("avatar");

    let avatarId = null;

    // 1. Если выбрано фото, загружаем его отдельно
    if (avatarFile && avatarFile.size > 0) {
      const imageForm = new FormData();
      imageForm.append("image", avatarFile);

      try {
        const res = await fetch("/api/v1/images/", {
          method: "POST",
          body: imageForm,
        });
        if (!res.ok) {
          throw new Error("Ошибка загрузки аватара");
        }
        const imgData = await res.json();
        avatarId = imgData.id;
      } catch (err) {
        errorBox.textContent = err.message;
        errorBox.classList.remove("hidden");
        return;
      }
    }

    // 2. Создаём объект юзера
    const userPayload = {
      username,
      email,
      password,
      avatar: avatarId, // может быть null
    };

    // 3. Отправляем регистрацию
    try {
      const res = await fetch("/api/v1/registration/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userPayload),
      });

      const data = await res.json();

      if (!res.ok) {
        errorBox.textContent = data.detail || JSON.stringify(data);
        errorBox.classList.remove("hidden");
        return;
      }

      alert("Регистрация успешна! Проверьте почту для активации.");
      regModal.close();
    } catch (err) {
      errorBox.textContent = "Ошибка соединения: " + err.message;
      errorBox.classList.remove("hidden");
    }
  });
});
