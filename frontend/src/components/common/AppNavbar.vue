<template>

<header
class="
bg-blue-800
text-white
"
>

<div
class="
max-w-7xl
mx-auto
h-16
flex
items-center
justify-between
px-8
"
>

<!-- 로고 -->

<RouterLink
to="/"
class="
text-2xl
font-bold
"
>

CardFit

</RouterLink>


<!-- 메뉴 -->

<nav
class="
flex
gap-10
text-sm
"
>

<RouterLink
to="/"
class="hover:text-blue-200"
>
홈
</RouterLink>

<RouterLink
to="/report"
class="hover:text-blue-200"
>
소비 분석
</RouterLink>

<RouterLink
to="/cards"
class="hover:text-blue-200"
>
카드 검색
</RouterLink>

<RouterLink
to="/compare"
class="hover:text-blue-200"
>
리포트
</RouterLink>

</nav>


<!-- 우측 -->

<RouterLink
to="/profile"
class="
bg-blue-700
px-5
py-2
rounded-full
text-sm
"
>

마이페이지

</RouterLink>

</div>

</header>

</template>

<script setup>

import { RouterLink }
from 'vue-router'

</script>