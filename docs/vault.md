# Securing Passwords with Ansible Vault

Ansible Vault provides a robust solution for encrypting sensitive information like node passwords within your project. This ensures your credentials remain secure, even if your code repository is exposed. Here's a detailed guide on utilizing Ansible Vault

<img src="https://images.photowall.com/products/49086/vault.jpg?h=699&q=85" width="30%" />

## How?

### First method

1. **Create a vault file:**
* Open a terminal and navigate to your project directory.
* Run the following command to create a new vault file named vaults/vault.yml
```
ansible-vault create vaults/vault.yml
```
This command initializes an empty vault file encrypted with a randomly generated key.<br/>

2. **Adding Passwords to the Vault:**

* Use the following command to edit the vault file:
```
ansible-vault edit vaults/vault.yml
```

This will open your default text editor (usually vi or nano) with the vault file content.
* Inside the editor, add your passwords as key-value pairs. For example, to store your Quilibrium node password:

```
quilibrium_password: "<your_strong_password>"
```

* Replace ```<your_strong_password>``` with your password.
* Save and close the editor. The passwords are now securely encrypted within the vault file.

3. **Referencing passwords from Inventory:**

* Update your [```inventory```](inventory.md) file to reference the password tag from the vault. Modify the ansible_password variable like this:

```
nodes:
  vars:
    ansible_password: '{{ quilibrium_password }}'  # Reference from vault
  hosts:
    # ... (Your node definitions)
```

4. **Managing the Vault File:**

* To edit the vault and update passwords:

```
ansible-vault edit vaults/vault.yml
```

* To view the contents of the vault file in a decrypted format:

```
ansible-vault view vaults/vault.yml
```

### Second method

1. Create an empty file called ```vault.yml``` into the directory ```vaults```.
2. Fill in this file with your password in plain text:
```
quilibrium_password: "<your_strong_password>"
```
3. Encrypt the ```vaults/vault.yml``` file with this command:
```
ansible-vault ansible encrypt vaults/vault.yml
```

## Official documentation

Find more information about vault encryption here:  https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#encrypting-files-with-ansible-vault

## Additional Security Best Practices:

* **Limit Vault Access:** Restrict access to the vault file itself. Consider storing it outside your version control system (e.g., Git) to prevent accidental exposure.
* **Regular Password Rotation:** Implement a regular password rotation schedule for your node passwords and update them within the vault accordingly.
* **Vault Password Management:** Choose a strong password for the vault itself and consider using a password manager to store it securely.

By following these steps and best practices, you can effectively secure your node passwords within the Quilibrium Tools project, enhancing the overall security posture of your Quilibrium node management.