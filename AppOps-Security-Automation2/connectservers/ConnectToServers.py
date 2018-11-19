import paramiko
import os

def connectservers(ipaddress, username, password, hostname):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ipaddress, 22, username, password)
        print("check status %s OK\n" % ipaddress)
        folder = os.getcwd()[:-4]+'/'+ipaddress
        print(folder)
        list = []
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ps -ef|grep java')
        listresult = ssh_stdout.readlines()
        print(listresult)
        host = hostname.split('.')
        host1 = host[0]
        #os.mkdir(ipaddress)
        if not os.path.exists(ipaddress):
            os.mkdir(ipaddress)
        for item in listresult:
            if '/IBM/WebSphere/AppServer' in item:
                list.append(item)
            #path1 = listresult.split('/')[1]

               # if not os.path.exists(ipaddress):
                    #os.makedirs(ipaddress)
                fo = open(ipaddress + "/CheckWAS.txt", "w")
                #fo = open("CheckWAS.txt", "w")
                fo.write(item)
                fo.close()

            # else:
            #    print('no WAS info')
        path2='/'.join(list)

        print(len(list))
        if len(list) <= 0:
            print('WAS is not installed')
        else:
            path1 = path2.split('/')[1]
            print('WAS is installed')
            fo = open(ipaddress + "/WASInfo.txt", "w")
            #fo = open("WASInfo.txt", "w")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cd /'+path1+'/IBM/WebSphere/AppServer/bin ; ./versionInfo.sh')
            if (len(ssh_stdout.readlines()) > 0):
                print('WAS information')
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cd /'+path1+'/IBM/WebSphere/AppServer/bin ; ./versionInfo.sh')
                for item in ssh_stdout.readlines():
                    fo.write(''.join(item))
                    if 'IBM WebSphere Application Server Network Deployment' in item:
                        print(item)
            fo.close()

            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cd /'+path1+'/IBM/WebSphere/AppServer/profiles ; ls ')
            for item in ssh_stdout.readlines():
                # print(item)
                item1 = item.strip('\n')
                if not os.path.exists(ipaddress + '/' + item1):
                    os.mkdir(ipaddress + '/' + item1)
                # pathming=os.getcwd()
                # os.mkdir(ipaddress+'/'+item1)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ps -ef|grep ' + item1)
                if len(ssh_stdout.readlines()) > 0:
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                        'cd /'+path1+'/IBM/WebSphere/AppServer/profiles/' + item1 + '/config/cells/; ls')
                    for cell in ssh_stdout.readlines():
                        if not "." in cell:
                            fo1 = open(ipaddress + '/' + item1 + '/' + item1 + '.txt', mode='w')
                            # fo2 = open(item1 + 'chmodsecurity.txt', mode='w')

                            commandline = r'head -2 /'+path1+'/IBM/WebSphere/AppServer/profiles/' + item1 + '/config/cells/' + cell.strip(
                                '\n') + '/security.xml'
                            print(commandline)
                            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(commandline)
                            # fo1.write(line.encode('utf-8'))
                            fo1.write(commandline + '\n')
                            for items in ssh_stdout.readlines():
                                fo1.write(items)
                            fo1.close()
                            # if not "." in ssh_stdout.readlines():

                            commandline2 = 'cd /'+path1+'/IBM/WebSphere/AppServer/profiles/%s/config/cells;ls' % (
                                item1.strip('\n'))
                            print(commandline2)
                        else:
                            continue
                        # commandline3 = 'cd /opt/IBM/WebSphere/AppServer/profiles/MF8Server01/config/cells/cnwbzp0253Cell01;ls -l security.xml'
                        # print(commandline3)
                        # cmd = r'cd /opt/IBM/WebSphere/AppServer/profiles/MF8Server01/config/cells/cnwbzp0253Cell01 ; ls -l security.xml'
                        # print(cmd)
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(commandline2)
                        for num1 in ssh_stdout.readlines():
                            if not "." in num1:
                                cmd = 'cd /'+path1+'/IBM/WebSphere/AppServer/profiles/%s/config/cells/%s;ls -l security.xml' % (
                                    item1.strip('\n'), num1.strip('\n'))
                                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
                                fo = open(ipaddress + '/' + item1 + '/' + item1 + '.txt', mode='a')
                                fo.write(cmd + '\n')
                                for num in ssh_stdout.readlines():
                                    fo.write(num)
                                fo.close()
                            else:
                                continue
                                servercmd = 'cd /'+path1+'IBM/WebSphere/AppServer/profiles/%s/config/cells/%s/nodes/;ls' % (item1.strip('\n'), num1.strip('\n'))
                                # print(servercmd)
                                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(servercmd)
                                for node in ssh_stdout.readlines():
                                    node1 = node.strip('\n')
                                    if node1.find('Node') > 0:
                                        # print(node1)
                                        nodecmd = 'cd /'+path1+'IBM/WebSphere/AppServer/profiles/%s/config/cells/%s/nodes/%s/servers;ls' % (
                                            item1.strip('\n'), num1.strip('\n'), node.strip('\n'))
                                        # print(nodecmd)
                                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(nodecmd)
                                        for server in ssh_stdout.readlines():
                                            # print(server)
                                            server1 = server.strip('\n')
                                            # print(server1)
                                            if 'server' in server1:
                                                # print('111111server1')
                                                servercmd1 = 'cd /'+path1+'/IBM/WebSphere/AppServer/profiles/%s/config/cells/%s/nodes/%s/servers/%s;ls -l server.xml' % (
                                                    item1.strip('\n'), num1.strip('\n'), node.strip('\n'), server1)
                                                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(servercmd1)
                                                fo4 = open(ipaddress + '/' + item1 + '/' + item1 + '.txt', mode='a')
                                                # print(ssh_stdout.readlines())
                                                fo4.write(servercmd1 + '\n')
                                                for access in ssh_stdout.readlines():
                                                    # print(type(access))
                                                    # print('sss' + access)
                                                    fo4.write(access)
                                                fo4.close()
                logcmd = 'cd /'+path1+'/IBM/WebSphere/AppServer/profiles/' + item1.strip('\n')+'/logs;ls -lR|grep .log$'

                #print(logcmd)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(logcmd)
                fo2 = open(ipaddress+'/'+item1+'/'+item1 + '.txt', mode='a')
                #print(ssh_stdout.readlines())
                fo2.write(logcmd+'\n')
                for log in ssh_stdout.readlines():

                    fo2.write(log)
                fo2.close()

                propertycmd = "cd /"+path1+"/IBM/WebSphere/AppServer/profiles/%s/properties;ls -l | egrep 'client.policy|sas.client.props|sas.stdclient.properties|sas.tools.properties|soap.client.props|wsadmin.properties|wsjaas_client.conf|client_types.xml|TraceSettings.properties'" %(item1.strip('\n'))

                print('sssdddd'+propertycmd)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(propertycmd)
                fo3 = open(ipaddress+'/'+item1+'/'+item1 + '.txt', mode='a')
                # print(ssh_stdout.readlines())
                fo3.write(propertycmd+'\n')
                for properties in ssh_stdout.readlines():
                    print(properties)
                    fo3.write(properties)
                fo3.close()

                soappropertycmd = "cd /"+path1+"/IBM/WebSphere/AppServer/profiles/%s/properties;grep com.ibm.SOAP.login soap.client.props" % (item1.strip('\n'))

                print('sssdddd' + soappropertycmd)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(soappropertycmd)
                fo6 = open(ipaddress+'/'+item1+'/'+item1 + '.txt', mode='a')
                # print(ssh_stdout.readlines())
                fo6.write(soappropertycmd+'\n')
                for properties in ssh_stdout.readlines():
                    print(properties)
                    fo6.write(properties)
                fo6.close()

                corbapropertycmd = "cd /"+path1+"/IBM/WebSphere/AppServer/profiles/%s/properties;grep com.ibm.CORBA.login sas.client.props" % (item1.strip('\n'))

                print('sssdddd' + corbapropertycmd)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(corbapropertycmd)
                fo7 = open(ipaddress+'/'+item1+'/'+item1 + '.txt', mode='a')
                fo7.write(corbapropertycmd+'\n')
                # print(ssh_stdout.readlines())
                for properties in ssh_stdout.readlines():
                    print(properties)
                    fo7.write(properties)
                fo7.close()

                etccmd = "cd /"+path1+"/IBM/WebSphere/AppServer/profiles/%s/etc;ls -l *p12" % (item1.strip('\n'))

                print('sssdddd' + etccmd)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(etccmd)
                fo8 = open(ipaddress+'/'+item1+'/'+item1 + '.txt', mode='a')
                # print(ssh_stdout.readlines())
                fo8.write(etccmd+'\n')
                for etc in ssh_stdout.readlines():
                    print(etc)
                    fo8.write(etc)
                fo8.close()

                chagecmd = "cd /"+path1+"/IBM/WebSphere/AppServer;ls -l"

                print('sssdddd' + chagecmd)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(chagecmd)
                fo9 = open(ipaddress + '/' +item1+'/'+item1 + '.txt', mode='a')
                # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(chagecmd)
                fo9.write(chagecmd+'\n')
                for chage in ssh_stdout.readlines():
                    if 'profiles' in chage:
                        s = chage.split()[3]
                        cmd = 'chage -l ' + s
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
                        for s in ssh_stdout.readlines():
                            fo9.write(s)
                fo9.close()

    except ConnectionError as ex:
        print(ex.__module__)
        print('connect to servers failed')
        return False
