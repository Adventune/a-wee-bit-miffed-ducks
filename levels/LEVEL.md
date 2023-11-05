# Level files

Level files contain data for initial state of level. They are written in JSON format.

## Level file structure

Level file is a JSON object with following fields 
(ignore TS definition, it was just easy for me to understand it that way):

```typescript
interface Level{
    name: string
    description: string,
    ducks: number,
    objects: [
        {
            type: "soft" | "hard" | "unbreakable" | "donkey" | "text",
            x: number,
            y: number,
            text?: string
        }
    ]
}
```
