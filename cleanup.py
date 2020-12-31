import subprocess


class FreeSpace():
    def __init__(self):
        self.imagesinfo = self.get_images_size_info()
        self.delete_images()

    def get_images_size_info(self):
        images = subprocess.run(
            ['docker', 'image', 'ls'],
            stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')

        filteredlist = []
        for image in images[1:len(images) - 1]:
            filteredinfo = list(filter(('').__ne__, image.split(' ')))
            infoLen = len(filteredinfo)

            filteredinfo = [filteredinfo[2], filteredinfo[3:infoLen-1], filteredinfo[infoLen-1]]
            if filteredinfo not in filteredlist:
                filteredlist.append(filteredinfo)

        return filteredlist

    def delete_images(self):
        for i in self.imagesinfo:
            if 'week' in i[1][1]:
                if int(i[1][0]) >= 2:
                    self.pipe_delete(i)
            elif 'month' in i[1][1] or 'year' in i[1][1]:
                self.pipe_delete(i)

        self.prune()

    def pipe_delete(self, info):
        """If an image cannot be deleted due to dependencies or running
        container, this script will not stop and throw an error.
        """
        d = subprocess.run(
            ['docker', 'image', 'rm', '-f', info[0]],
            stdout=subprocess.PIPE).stdout.decode('utf-8')

        print("Image deletion output:", d)

    def prune(self):
        p = subprocess.run(
            ['docker', 'system', 'prune', '-f', '--volumes'],
            stdout=subprocess.PIPE).stdout.decode('utf-8')

        print("Prune output:", p)

cleanup = FreeSpace()
