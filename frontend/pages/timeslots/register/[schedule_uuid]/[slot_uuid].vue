<template>
<div v-if="slot">
    {{ formatTime(new Date(slot.begin_time)) }}
    {{ formatTime(new Date(slot.end_time)) }}
    <form action="" method="post" @submit.prevent="saveRegistration" class="container bg-slate-200 h-100">
        <input type="text" v-model="comment" name="comment" id="comment"/>
        <select v-model="courseSelect" name="courses" id="courses">
            <option v-for="course in courses">{{ course.name }}</option>
        </select>
        <input type="hidden" :value="slot"/>
        <input type="hidden" v-if="user" :value="user"/>
        <input type="submit" value="Submit" class="mx-1 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full">
    </form>
</div>
</template>
<script lang="ts">
import { ref, onMounted } from 'vue';

// recuperer user
import { userStore } from "~/stores/user";
    export default {
        
        setup() {
            const route = useRoute();
            const slot_uuid = route.params.slot_uuid as string;
            const schedule_uuid = route.params.schedule_uuid as string;
            const user = userStore().user;
            
            const slot = ref<ITimeslots | null>(null);
            const schedule = ref<ISchedules | null>(null);
            const courses = ref<ICourses[] | null>(null);
            const comment = ref('');
            const courseSelect = ref<ICourses | null>(null);

            const fetchTimeSlots = async (uuid: string) => {
            try {
                const { data: aslots } = await useAPI<ITimeslots[] | null>(
                `/timeslots/${uuid}/`
                );
                if (aslots?.value) {
                slot.value = aslots.value.filter((ts) => ts.uuid === slot_uuid)[0];
                }
            } catch (error) {
                console.error("Erreur lors de la récupération des créneaux : ", error);
            }
            };

            const fetchSchedules = async (uuid:string) => {
                const { data : aschedule } = await useAPI<ISchedules | null>(
                    `/schedules/${schedule_uuid}`
                )
                schedule.value = aschedule.value
            }

            function formatTime(d: Date) {
                let hours = d.getHours();
                let minutes = d.getMinutes();
                const lzero = (d: number) => `${d < 10 ? "0" : ""}${d}`;
                return `${lzero(hours)}:${lzero(minutes)}`;
            }

            const fetchCourses = async(uuid: string) => {
                const { data: acourses } = await useAPI<ICourses[] | null>(
                    `/courses/${uuid}/courses`
                )
                courses.value = acourses.value
            }

            const saveRegistration = async () => {
                if (!courseSelect.value || !comment.value) {
                    console.error("Veuillez remplir tous les champs");
                    return;
                }

                // Création des données à envoyer
                const data = {
                    comment: comment.value,
                    course: courseSelect.value,
                    slot: slot.value,
                    student: user
                };

                try {
                    // Envoi de la requête POST
                    const response = await useAPI<unknown>('/registrations/add/', {
                        method: 'POST',
                        body: data
                    });

                    console.log("Enregistrement effectué avec succès", response);
                } catch (error) {
                    console.error("Erreur lors de l'enregistrement", error);
                }
            };

            onMounted(async () => {
                await fetchTimeSlots(schedule_uuid);
                await fetchSchedules(schedule_uuid);
                if(schedule.value){
                    const teacher_uuid = schedule.value.teacher.uuid
                    await fetchCourses(teacher_uuid);
                }else{
                }
            });

            return {
            slot,schedule,courses,user,
            comment,
            courseSelect,
            formatTime,
            saveRegistration
            };
        },
    };
</script>