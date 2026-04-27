# Vitest Matchers Cheatsheet

```ts
// Equality
expect(value).toBe(42)              // strict ===
expect(value).toEqual({ a: 1 })    // deep equality
expect(value).toStrictEqual(obj)   // deep + same type

// Truthiness
expect(value).toBeTruthy()
expect(value).toBeFalsy()
expect(value).toBeNull()
expect(value).toBeUndefined()
expect(value).toBeDefined()

// Numbers
expect(n).toBeGreaterThan(0)
expect(n).toBeCloseTo(3.14, 2)     // float precision

// Strings
expect(str).toContain('hello')
expect(str).toMatch(/pattern/)

// Arrays
expect(arr).toHaveLength(3)
expect(arr).toContain('item')
expect(arr).toEqual(expect.arrayContaining(['a', 'b']))

// Objects
expect(obj).toHaveProperty('key', 'value')
expect(obj).toMatchObject({ a: 1 }) // partial match

// Functions / errors
expect(() => fn()).toThrow()
expect(() => fn()).toThrow('message')
expect(() => fn()).toThrow(ErrorClass)

// Promises
await expect(promise).resolves.toBe('value')
await expect(promise).rejects.toThrow('error')

// Mocks
expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledOnce()
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2')
expect(mockFn).toHaveBeenCalledTimes(3)
expect(mockFn).toHaveReturnedWith('value')
```
