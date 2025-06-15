InsightUI.Modal = {
  init: function () {
    document.querySelectorAll('[data-insight-toggle="modal"]').forEach(button => {
      button.addEventListener('click', function () {
        const targetId = this.getAttribute('data-insight-target');
        const modal = document.getElementById(targetId);
        if (modal) {
          modal.classList.remove('hidden');
          modal.querySelector('[data-insight-dismiss="modal"]').addEventListener('click', function () {
            modal.classList.add('hidden');
          });
          InsightUI.utils.trapFocus(modal);
        }
      });
    });
  }
};
document.addEventListener('DOMContentLoaded', InsightUI.Modal.init);
