class P:
    ...     def initialize(self):
        ...         self.dosomthing()
                    ...     def dosomthing(self):
                        ...         print "call from parent"
                                    ... class C(P):
                                        ...     def dosomthing(self):
                                            ...         print "call from child"
                                                        >>> c = C()
                                                        >>> c.initialize()
                                                        call from child
                                                        >>> class P_with_private:
                                                            ...     def initialize(self):
                                                                ...         self.__dosomthing()
                                                                            ...     def __dosomthing(self):
                                                                                ...         print "call from parent"
                                                                                            ... class C2(P_with_private):
                                                                                                ...     def __dosomthing(self):
                                                                                                    ...         print "call from child"
                                                                                                                >>> c2 = C2()
                                                                                                                >>> c2.initialize()
                                                                                                                call from parent
                                                                                                                >>> class P_with_hint:
                                                                                                                    ...     def initialize(self):
                                                                                                                        ...         self._dosomthing()
                                                                                                                                    ...     def _dosomthing(self):
                                                                                                                                        ...         print "call from parent"
                                                                                                                                                    ... class C3(P_with_hint):
                                                                                                                                                        ...     def _dosomthing(self):
                                                                                                                                                            ...         print "call from child"
                                                                                                                                                                        >>> c3 = C3()
                                                                                                                                                                        >>> c3.initialize()
                                                                                                                                                                        call from child
