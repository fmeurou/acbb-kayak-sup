(function () {
	"use strict";

	var navToggle = document.querySelector(".nav-toggle");
	var siteNav = document.getElementById("site-nav");

	if (navToggle && siteNav) {
		navToggle.addEventListener("click", function () {
			var isOpen = siteNav.classList.toggle("is-open");
			navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
		});

		siteNav.addEventListener("click", function (event) {
			if (event.target.tagName === "A") {
				siteNav.classList.remove("is-open");
				navToggle.setAttribute("aria-expanded", "false");
			}
		});
	}

	var backToTop = document.getElementById("back-to-top");

	if (backToTop) {
		var toggleBackToTop = function () {
			backToTop.classList.toggle("on", window.scrollY > 400);
		};
		window.addEventListener("scroll", toggleBackToTop, { passive: true });
		toggleBackToTop();

		backToTop.addEventListener("click", function () {
			window.scrollTo({ top: 0, behavior: "smooth" });
		});
	}

	var carousels = document.querySelectorAll(".article_carousel");

	if (carousels.length) {
		var lightbox = document.createElement("div");
		lightbox.className = "lightbox";
		lightbox.innerHTML =
			'<button type="button" class="lightbox-close" aria-label="Fermer">&times;</button>' +
			'<button type="button" class="lightbox-prev" aria-label="Image précédente">&#8249;</button>' +
			'<img alt="">' +
			'<button type="button" class="lightbox-next" aria-label="Image suivante">&#8250;</button>';
		document.body.appendChild(lightbox);

		var lightboxImg = lightbox.querySelector("img");
		var activeImgs = [];
		var activeIndex = 0;

		var showImage = function () {
			var img = activeImgs[activeIndex];
			lightboxImg.src = img.src;
			lightboxImg.alt = img.alt;
		};
		var openLightbox = function (imgs, index) {
			activeImgs = imgs;
			activeIndex = index;
			showImage();
			lightbox.classList.add("is-open");
		};
		var closeLightbox = function () {
			lightbox.classList.remove("is-open");
		};
		var step = function (delta) {
			activeIndex = (activeIndex + delta + activeImgs.length) % activeImgs.length;
			showImage();
		};

		lightbox.querySelector(".lightbox-close").addEventListener("click", closeLightbox);
		lightbox.querySelector(".lightbox-prev").addEventListener("click", function () { step(-1); });
		lightbox.querySelector(".lightbox-next").addEventListener("click", function () { step(1); });
		lightbox.addEventListener("click", function (event) {
			if (event.target === lightbox) closeLightbox();
		});
		document.addEventListener("keydown", function (event) {
			if (!lightbox.classList.contains("is-open")) return;
			if (event.key === "Escape") closeLightbox();
			else if (event.key === "ArrowLeft") step(-1);
			else if (event.key === "ArrowRight") step(1);
		});

		carousels.forEach(function (carousel) {
			var imgs = Array.prototype.slice.call(carousel.querySelectorAll("img"));
			if (!imgs.length) return;

			imgs.forEach(function (img, index) {
				img.addEventListener("click", function () {
					openLightbox(imgs, index);
				});
			});

			if (imgs.length < 2) return;

			var timer = null;
			var advance = function () {
				var maxScroll = carousel.scrollWidth - carousel.clientWidth;
				var step = imgs[0].getBoundingClientRect().width + 10;
				var next = carousel.scrollLeft + step;
				carousel.scrollTo({ left: next > maxScroll - 5 ? 0 : next, behavior: "smooth" });
			};
			var start = function () {
				if (!timer) timer = window.setInterval(advance, 2000);
			};
			var stop = function () {
				window.clearInterval(timer);
				timer = null;
			};

			start();
			carousel.addEventListener("mouseenter", stop);
			carousel.addEventListener("mouseleave", start);
			carousel.addEventListener("touchstart", stop, { passive: true });
		});
	}
})();
