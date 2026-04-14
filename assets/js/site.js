(function () {
    function initThemeToggle() {
        var themeToggle = document.getElementById('themeToggle');
        if (!themeToggle) {
            return;
        }

        var icon = themeToggle.querySelector('i');

        function setTheme(isDark) {
            document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
            if (icon) {
                icon.classList.toggle('fa-sun', isDark);
                icon.classList.toggle('fa-moon', !isDark);
            }
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        }

        var savedTheme = localStorage.getItem('theme');
        var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(savedTheme ? savedTheme === 'dark' : prefersDark);

        themeToggle.addEventListener('click', function () {
            var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            setTheme(!isDark);
        });
    }

    function initSectionReveal() {
        var sections = document.querySelectorAll('.section');
        if (!sections.length) {
            return;
        }

        if ('IntersectionObserver' in window) {
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            sections.forEach(function (el) {
                observer.observe(el);
            });
        } else {
            sections.forEach(function (el) {
                el.classList.add('visible');
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        initThemeToggle();
        initSectionReveal();
    });

    window.initSiteCommon = {
        initThemeToggle: initThemeToggle,
        initSectionReveal: initSectionReveal
    };
})();
