let currentLang = "es";

const translations = {
    es: {
        nav_inicio: "INICIO",
        nav_nosotros: "SOBRE NOSOTROS",
        nav_recetario: "RECETARIO",
        nav_integrantes: "INTEGRANTES",
        nav_cerrar: "CERRAR SESIÓN",
        nav_iniciar: "INICIAR SESIÓN",
        main_titulo: "PÁGINA PRINCIPAL",
        main_desc1:
            "GastroLab es la plataforma digital del centro. Aquí encontrarás recetas, menús semanales y contenido exclusivo, todo en un solo lugar.",
        main_desc2:
            "La gastronomía también se digitaliza. En GastroLab encontrarás recetas, menús y contenido exclusivo del centro, todo organizado en un solo sitio. Porque perder una receta entre papeles ya es historia.",
        footer_contacto: "Contacto",
        iniciar_sesion: "Iniciar Sesión",
        acceder: "Accede a tu cuenta de GastroLab",
        no_cuenta: "No tienes cuenta?",
        registro: "Registrate",
        mensaje_error: "Introduce credenciales correctas",
    },
    en: {
        nav_inicio: "HOME",
        nav_nosotros: "ABOUT US",
        nav_recetario: "RECIPE BOOK",
        nav_integrantes: "MEMBERS",
        nav_cerrar: "LOG OUT",
        nav_iniciar: "LOG IN",
        main_titulo: "MAIN PAGE",
        main_desc1:
            "GastroLab is the culinary center's digital platform. Here you'll find recipes, weekly menus and exclusive content, all in one place.",
        main_desc2:
            "Gastronomy goes digital. On GastroLab you'll find recipes, menus and exclusive content from the center, all organized in one place. Because losing a recipe in a pile of papers is history.",
        footer_contacto: "Contact",
        iniciar_sesion: "Log In",
        acceder: "Access your GastroLab account",
        no_cuenta: "Don't have an account?",
        registro: "Register",
        mensaje_error: "Introduce correct credencials",
    },
};

function toggleLang() {
    currentLang = currentLang === "es" ? "en" : "es";
    const isEn = currentLang === "en";
    document.getElementById("langBtn").textContent = isEn
        ? " Español"
        : " English";
    document.querySelectorAll("[data-i18n]").forEach((el) => {
        const key = el.getAttribute("data-i18n");
        if (translations[currentLang][key]) {
            el.textContent = translations[currentLang][key];
        }
    });
}
