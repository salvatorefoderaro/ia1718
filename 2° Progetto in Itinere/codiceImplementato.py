    def controlloFunzione(self):
        nodi = []
        nodeMax = [0, 0]
        for nodo in (self.getNodes()):
            if (self.getAdjModified(nodo.id) != 0):
                nodi.append(nodo.id)

        while (len(nodi)>0):
            percorso = self.mediumNode(random.choice(nodi))
            if percorso[1] != 0:
                nodoMassimo = self.backToFather(percorso[1], percorso[3])
                if(nodoMassimo != 0 and nodoMassimo[1] > nodeMax[1]):
                    nodeMax[0] = nodoMassimo[0]
                    nodeMax[1] = nodoMassimo[1]
            nodi = list(set(nodi) - set(percorso[2]))

        return nodeMax

    def backToFather(self, rootID, percorso):
        nodeList = [0, 0]
        #percorso = []  # La lista dei nodi appartenenti al percorso più lungo
        #while (rootID.father != None and rootID != int):  # Fin quando il nodo che sto considerando ha un padre,
        #    percorso.append(rootID.info)  # aggiungo il padre alla lista dei nodi appartenenti al percorso,
        #    rootID = rootID.father  # imposto il padre come nuovo nodo

        if len(percorso) < 3:  # Se ho meno di tre elementi nel percorso, nessun nodo risulta medio
            return 0

        if (len(percorso) % 2) == 0:  # Se il numero di elementi è pari, devo controllare quale dei due elementi ha il maggior numero di figli

            # Ottengo i due elementi medi nella lista
            primoElemento = percorso[int(len(percorso) / 2)]
            secondoElemento = percorso[int((len(percorso) / 2) + 1)]

            # Elimino l'arco che collega i due nodi, in modo da poter eseguire due visite separate
            self.deleteEdge(primoElemento, secondoElemento)
            self.deleteEdge(secondoElemento, primoElemento)

            first = self.calculateSubNode(primoElemento)  # Numero di nodi figli del primo elemento
            second = self.calculateSubNode(secondoElemento)  # Numero di nodi figli del secondo elemento
            # Devo aggiungere il return della lunghezza del percorso
            if first < second:
                nodeList = [secondoElemento, second]
            elif second > first:
                nodeList = [primoElemento, first]
            else:
                nodeList = [[primoElemento, secondoElemento], first]
        else:
                nodeList = [percorso[int(len(percorso)/2)], int(len(percorso)/2)]
        return nodeList

    def calculateSubNode(self, rootId):
        """
        Execute a generic search in the graph starting from the specified node.
        :param rootId: the root node ID (integer).
        :return: the generic exploration tree.
        """

        counter = 0  # Contatore degli elementi figli del nodo

        # Utilizzo l'algoritmo per la visita generica visto a lezione
        if rootId not in self.nodes:
            return None

        treeNode = TreeNode(rootId)
        vertexSet = {treeNode}
        markedNodes = {rootId}

        while len(vertexSet) > 0:
            treeNode = vertexSet.pop()
            adjacentNodes = self.getAdj(treeNode.info)
            for nodeIndex in adjacentNodes:
                if nodeIndex not in markedNodes:
                    counter = counter + 1  # Incremento il contatore
                    newTreeNode = TreeNode(nodeIndex)
                    vertexSet.add(newTreeNode)
                    markedNodes.add(nodeIndex)
        return counter

    def mediumNode(self, rootId):
        """
        Execute a generic search in the graph starting from the specified node.
        :param rootId: the root node ID (integer).
        :return: the generic exploration tree.
        """

        max = [0, 0, 0, 0]  # Inizializzo a 0 le informazioni riguardo al nodo massimo

        # Utilizzando l'algoritmo per la visita generica visto a lezione, scansiono l'albero
        if rootId not in self.nodes:
            return None

        treeNode = TreeNode(rootId)
        vertexSet = {treeNode}
        markedNodes = [rootId]  # Nodi visitati

        while len(vertexSet) > 0:
            treeNode = vertexSet.pop()
            adjacentNodes = self.getAdj(treeNode.info)

            if len(
                    adjacentNodes) == 1:  # Se il nodo che sto considerando ha solamente un nodo adiacente, dunque è una foglia:
                lunghezzaPercorso = self.leafDistance(
                    treeNode.info)  # Calcolo la lunghezza del percorso massimo raggiungibile dalla foglia
                if lunghezzaPercorso[0] > max[
                    0]:  # Se il percorso è più lungo dell'attuale massimo, imposto i valori della foglia
                    max[0] = lunghezzaPercorso[0]
                    max[1] = lunghezzaPercorso[1]
                    max[3] = lunghezzaPercorso[2]

            for nodeIndex in adjacentNodes:
                if nodeIndex not in markedNodes:
                    newTreeNode = TreeNode(nodeIndex)
                    newTreeNode.father = treeNode
                    treeNode.sons.append(newTreeNode)
                    vertexSet.add(newTreeNode)
                    markedNodes.append(nodeIndex)

        max[2] = markedNodes
        return max

    def leafDistance(self, rootId):
        """
        Execute a generic search in the graph starting from the specified node.
        :param rootId: the root node ID (integer).
        :return: the generic exploration tree.
        """

        lunghezzaPercorso = [0, 0, 0]
        # lunghezzaPercorso[0] = distanza del nodo dalla radice
        # lunghezzaPercorso[1] = nodo

        # Eseguo una visita generica utilizzando l'algoritmo visto a lezione
        if rootId not in self.nodes:
            return None

        treeNode = TreeNode(rootId)
        vertexSet = {treeNode}
        markedNodes = [rootId]

        while len(vertexSet) > 0:
            treeNode = vertexSet.pop()
            adjacentNodes = self.getAdj(treeNode.info)

            if len(
                    adjacentNodes) == 1:  # Quando trovo una foglia, controllo la sua distanza dalla foglia considerata in questo caso come radice
                if lunghezzaPercorso[
                    0] < treeNode.distanza:  # Se la foglia ha una distanza superiore a quella dell'attuale percorso, imposto i nuovi valori
                    lunghezzaPercorso[0] = treeNode.distanza
                    lunghezzaPercorso[1] = treeNode
                elif lunghezzaPercorso[0] == treeNode.distanza:
                    lunghezzaPercorso[0] = treeNode.distanza
                    lunghezzaPercorso[1] = treeNode

            for nodeIndex in adjacentNodes:
                if nodeIndex not in markedNodes:
                    newTreeNode = TreeNode(nodeIndex)
                    newTreeNode.father = treeNode
                    newTreeNode.distanza = treeNode.distanza + 1  # Incremento la distanza del nodo
                    treeNode.sons.append(newTreeNode)
                    vertexSet.add(newTreeNode)
                    markedNodes.append(nodeIndex)
        lunghezzaPercorso[2] = markedNodes

        return lunghezzaPercorso  # Restituisco la lista con i valori