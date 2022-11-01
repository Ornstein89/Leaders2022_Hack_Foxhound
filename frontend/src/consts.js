export const STATUSES = [
    {
        text: "Ожидает подтверждения",
        value: "pending",
    },
    {
        text: "Отклонено",
        value: "declined",
    },
    {
        text: "Подтверждено",
        value: "approved",
    },
]
export function status_mapper(value) { return STATUSES.find(v => v.value == value).text}
