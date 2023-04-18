export const createStore = () => {
  const memberStore = {
    tokenKey: '',
    get getMemberToken() {
      return this.tokenKey
    },
    setMemberToken(newToken: string) {
      this.tokenKey = newToken
    }
  }
  return memberStore;
}

export default createStore;
export type TStore = ReturnType<typeof createStore>;