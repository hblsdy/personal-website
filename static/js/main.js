// 通用前端脚本
document.addEventListener("DOMContentLoaded", function () {
    console.log("Personal website loaded.");

    // 表单提交前简单验证
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
        form.addEventListener("submit", function (e) {
            const inputs = form.querySelectorAll("input[required]");
            for (const inp of inputs) {
                if (!inp.value.trim()) {
                    e.preventDefault();
                    inp.focus();
                    alert("请填写：" + (inp.previousElementSibling?.textContent || inp.placeholder));
                    return;
                }
            }
        });
    });
});
