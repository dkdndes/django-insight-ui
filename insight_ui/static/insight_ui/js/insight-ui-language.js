InsightUI.Language = {
  init: function () {
    const languageSelect = document.getElementById('language-select');
    if (!languageSelect) return;

    languageSelect.addEventListener('change', function () {
      const selectedLanguage = this.value;
      InsightUI.Language.changeLanguage(selectedLanguage);
    });
  },
  changeLanguage: function (languageCode) {
    const form = document.getElementById('language-form');
    const input = form.querySelector('input[name="language"]');
    input.value = languageCode;
    form.submit();
  }
};

document.addEventListener('DOMContentLoaded', InsightUI.Language.init);
