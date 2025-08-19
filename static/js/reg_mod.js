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
  const regBtn = document.getElementById("reg-btn");
  const regModal = document.getElementById("registerModal");
  const cancelBtn = document.getElementById("register-cancel");
  const regForm = document.getElementById("register-form");

  // открыть модалку
  regBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    regModal.showModal();
  });

  // закрыть модалку
  cancelBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    regModal.close();
  });

  // сабмит формы
  regForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    // создаём FormData из формы
    const formData = new FormData(regForm);

    try {
      const resp = await fetch("/api/v1/registration/", {
        method: "POST",
        body: formData, // Content-Type выставится автоматически
      });

      const data = await resp.json().catch(() => ({}));

      if (!resp.ok) {
        alert("Ошибка: " + (data.detail || JSON.stringify(data)));
        return;
      }

      alert("Регистрация успешна! Проверьте почту для активации.");
      regModal.close();
      regForm.reset(); // очищаем форму
    } catch (err) {
      alert("Ошибка соединения: " + err);
    }
  });
});
