<template>
    <b-table-simple small>
        <b-tr>
            <b-td 
            v-for="device in locationDevices" 
            :title="device.id" 
            :class="ping_code_class(device.ping_code)" 
            :key="device.id"
            v-on:click.stop="clicked(device)">
                <div class="overview-td">
                    {{ device.ping_code }}
                </div>
            </b-td>
        </b-tr>
    </b-table-simple>
</template>

<script>


export default {
    name: 'DevicesOverview',
    props: ["locationDevices", "location"],
    methods: {
        ping_code_class(value){
            if (value == 0){
                return "up"
            }
            else if (value == 1){
                return "dns"
            }
            else{
                return "down"
            }
        },
        clicked(item) {
            this.$emit("scan-device", item.id)
        }
    }
}
</script>

<style scoped>
table {
    margin: 0 0 0 5px;
    table-layout: fixed;
    border-collapse: separate;
    display: inherit;
}
.overview-td {
    height: 100%;
    width: 100%;
    overflow: hidden;
}
td {
    margin: 0 1px;
    width: 15px;
    height: 100%;
    overflow: hidden;
    display: inline-block;
    cursor: pointer;
}
.up, .down, .dns {
    border-radius: 0.25rem;
    cursor: pointer;
}
</style>
