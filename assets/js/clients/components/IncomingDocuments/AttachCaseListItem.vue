<template>
	<b-list-group-item>
		<b-row>
			<b-col cols="5" md="12" lg="6" class="mb-4 mb-md-0 text-left">
				<b-row>
					<b-col cols="12">
						<case-status-label :value="caseEntity" />

						<span class="font-weight-bold">
							<span v-if="caseEntity.admit_date">
								{{ $filters.formatDate(caseEntity.admit_date) }}
							</span>
							<span v-if="caseEntity.admit_date && caseEntity.discharge_date" class="text-muted">
								&mdash;
							</span>
							<span v-if="caseEntity.discharge_date">
								{{ $filters.formatDate(caseEntity.discharge_date) }}
							</span>
						</span>
					</b-col>
				</b-row>

				<p v-if="caseTypeName" class="small text-muted mb-0" title="Case Type">
					<span>{{ caseTypeName }}</span>
				</p>
				<p v-if="clientEmployeeName" class="small text-muted mb-0" title="Physician">
					<font-awesome-icon icon="user-md" fixed-width />
					<span>{{ clientEmployeeName }}</span>
				</p>
				<p v-if="facilityName" class="small text-muted mb-0" title="Facility">
					<font-awesome-icon icon="building" fixed-width />
					<span>{{ facilityName }}</span>
				</p>
			</b-col>
			<b-col cols="7" md="12" lg="6" class="mb-4 mb-md-0 text-right">
				<b-dropdown right menu-class="shadow" variant="primary">
					<template #button-content>
						<font-awesome-icon icon="plus" fixed-width />
						<span>New</span>
					</template>

					<b-dropdown-item
						@click="
							addingAppeal = true;
							addingRequest = false;
						"
						:active="addingAppeal"
					>
						<span>Appeal</span>
					</b-dropdown-item>

					<b-dropdown-item
						@click="
							addingRequest = true;
							addingAppeal = false;
						"
						:active="addingRequest"
					>
						<span>Request</span>
					</b-dropdown-item>
				</b-dropdown>

				<b-dropdown right menu-class="shadow" variant="secondary">
					<template #button-content>
						<font-awesome-icon icon="cog" fixed-width />
					</template>
					<b-dropdown-item :to="{ name: 'cases.view', params: { id: caseEntity.id } }">
						<font-awesome-icon icon="eye" fixed-width />
						<span>View Case</span>
					</b-dropdown-item>

					<b-dropdown-divider />

					<b-dropdown-item :to="{ name: 'cases.edit', params: { id: caseEntity.id } }">
						<font-awesome-icon icon="edit" fixed-width />
						<span>Edit Case</span>
					</b-dropdown-item>
				</b-dropdown>
			</b-col>
		</b-row>
		<b-row v-if="addingAppeal" class="my-2">
			<b-col cols="12">
				<appeal-form
					:case-entity="caseEntity"
					@saved="addedAppeal"
					@cancel="addingAppeal = false"
					class="shadow"
				>
					<template #header>
						<b-card-header>
							<div class="d-flex justify-content-between align-items-center">
								<span class="font-weight-bold">Add New Appeal</span>
								<b-button
									variant="secondary"
									size="sm"
									@click="addingAppeal = false"
									title="Cancel"
									class="mb-0"
								>
									<font-awesome-icon icon="remove" fixed-width class="my-0 py-0" />
								</b-button>
							</div>
						</b-card-header>
					</template>
				</appeal-form>
			</b-col>
		</b-row>
		<b-row v-else-if="addingRequest" class="my-2">
			<b-col cols="12">
				<case-request-form :case-entity="caseEntity" @saved="addedRequest" @cancel="addingRequest = false">
					<template #header>
						<b-card-header>
							<div class="d-flex justify-content-between align-items-center">
								<span class="font-weight-bold">Add New Request</span>
								<b-button
									variant="secondary"
									size="sm"
									@click="addingRequest = false"
									title="Cancel"
									class="mb-0"
								>
									<font-awesome-icon icon="remove" fixed-width class="my-0 py-0" />
								</b-button>
							</div>
						</b-card-header>
					</template>
				</case-request-form>
			</b-col>
		</b-row>
		<div v-else-if="hasAppeals || hasRequests" class="my-2">
			<div v-if="hasRequests">
				<b-card no-body>
					<b-card-header>Requests</b-card-header>
					<b-list-group flush>
						<b-list-group-item v-for="caseRequest in requests" :key="caseRequest.id" class="shadow-sm">
							<p class="font-weight-bold mb-0">
								<span v-if="caseRequest.name">
									{{ caseRequest.name }}
								</span>
							</p>
							<p class="mb-0 text-muted">
								<span v-if="caseRequest.type_label"> {{ caseRequest.type_label }} Request </span>
							</p>
							<p v-if="caseRequest.status_label !== 'Closed'" class="mb-0">
								<span
									v-if="caseRequest.due_date"
									class="small"
									:class="caseRequest.is_overdue ? 'text-danger font-weight-bold' : 'text-muted'"
								>
									Due on {{ $filters.formatDate(caseRequest.due_date) }}
								</span>
							</p>
						</b-list-group-item>
					</b-list-group>
				</b-card>
			</div>
			<div v-if="hasAppeals">
				<b-card no-body>
					<b-card-header>Appeals</b-card-header>
					<b-list-group flush>
						<b-list-group-item v-for="appeal in appeals" :key="appeal.id" class="shadow-sm">
							<b-row>
								<b-col cols="8" md="6" lg="12" xl="6" class="text-left mb-2 mb-md-0">
									<p class="mb-0">
										<span v-if="appeal.appeal_level && appeal.appeal_level.name">
											{{ appeal.appeal_level.name }}
										</span>
										<span v-else class="text-danger"> Missing Level </span>
										<span v-if="appeal.appeal_level && appeal.appeal_type" class="text-muted">
											&mdash;
										</span>
										<span v-if="appeal.appeal_type && appeal.appeal_type.name" class="text-muted">
											{{ appeal.appeal_type.name }}
										</span>
										<span v-else class="text-danger"> Missing Type </span>
										<appeal-status-label :value="appeal" />
									</p>
									<p v-if="appeal.appeal_status !== 'Closed'" class="mb-0">
										<span
											v-if="appeal.due_date"
											class="small"
											:class="appeal.is_overdue ? 'text-danger font-weight-bold' : 'text-muted'"
										>
											Due on {{ $filters.formatDate(appeal.due_date) }}
										</span>
									</p>
									<p v-if="appeal.modified" class="small text-muted mb-0">
										Last updated {{ $filters.formatTimestamp(appeal.modified) }}
									</p>
								</b-col>
								<b-col cols="4" md="6" lg="12" xl="6" class="text-right">
									<b-dropdown
										split
										right
										@click="attachToAppeal(appeal, { redirect: false })"
										:disabled="attaching"
										variant="primary"
									>
										<template #button-content>
											<font-awesome-icon icon="paperclip" fixed-width />
											<span>Attach</span>
										</template>
										<b-dropdown-item-button
											@click="attachToAppeal(appeal, { redirect: true })"
											:disabled="attaching"
											title="Attach and view appeal"
										>
											<div>Attach &amp; View</div>
											<small class="text-muted"> Attach document and view appeal after. </small>
										</b-dropdown-item-button>
									</b-dropdown>
								</b-col>
							</b-row>
						</b-list-group-item>
					</b-list-group>
				</b-card>
			</div>
		</div>
		<div v-else>
			<b-alert show variant="info" class="my-2">
				<font-awesome-icon icon="exclamation-triangle" fixed-width />
				No appeals or requests have been created for this case.
			</b-alert>
		</div>
	</b-list-group-item>
</template>

<script>
import AppealForm from "@/clients/components/Appeals/Form.vue";
import AppealStatusLabel from "@/clients/components/Appeals/StatusLabel.vue";
import CaseStatusLabel from "@/clients/components/Cases/StatusLabel.vue";
import CaseRequestForm from "@/clients/components/CaseRequests/Form.vue";

export default {
	name: "AttachCaseListItem",
	components: {
		AppealForm,
		AppealStatusLabel,
		CaseStatusLabel,
		CaseRequestForm,
	},
	props: {
		patient: {
			required: true,
			type: Object,
			default: () => {
				return {
					id: null,
					first_name: null,
					last_name: null,
					full_name: null,
					list_name: null,
				};
			},
		},
		caseEntity: {
			type: Object,
			default: () => {
				return {
					id: null,
					appeals: [],
					case_requests: [],
					case_type: {
						id: null,
						name: null,
					},
					facility: {
						id: null,
						name: null,
					},
				};
			},
		},
		document: {
			required: true,
			type: Object,
			default: () => {
				return {
					id: null,
					created: null,
				};
			},
		},
	},
	data() {
		return {
			addingAppeal: false,
			appeals: this.caseEntity.appeals || [],

			addingRequest: false,
			requests: this.caseEntity.requests || [],

			loading: false,
			attaching: false,
		};
	},
	computed: {
		caseTypeName() {
			return this.caseEntity.case_type?.name ?? "";
		},
		clientEmployeeName() {
			return this.caseEntity.client_employee?.full_name ?? "";
		},
		facilityName() {
			return this.caseEntity.facility?.name ?? "";
		},
		hasAppeals() {
			return this.appeals.length > 0;
		},
		hasRequests() {
			return this.requests.length > 0;
		},
	},
	methods: {
		addedAppeal(appeal) {
			this.addingAppeal = false;
			this.appeals.push(appeal);

			this.$emit("added-appeal", appeal);
		},
		addedRequest(request) {
			this.addingRequest = false;
			this.requests.push(request);

			this.$emit("added-request", request);
		},
		async attachToAppeal(appeal, options = {}) {
			try {
				this.attaching = true;

				const response = await this.$store.dispatch("incomingDocuments/attachAppeal", {
					id: this.document.id,
					case_id: appeal.case_id,
					appeal_id: appeal.id,
				});

				this.$emit("attached", response);

				if (options.redirect && options.redirect === true) {
					this.$router.push({
						name: "appeals.view",
						params: {
							id: appeal.case_id,
							appeal_id: appeal.id,
						},
					});
				}
			} catch (e) {
				this.$store.dispatch("apiError", {
					error: e,
					title: "Attach Failed",
					message: "An error occurred when attempting to attach to appeal.",
				});
			} finally {
				this.attaching = false;
			}
		},
		async attachToCase(caseEntity, options = {}) {
			let message = `Are you sure you want to merge the current document in with case #${caseEntity.id} (Admit Date: ${caseEntity.admit_date})?`;

			if (!redirectAfter) {
				message +=
					" The document will be removed from the queue and you will need to search the patient in order to find it again.";
			}

			if (!confirm(message)) {
				return false;
			}

			try {
				const response = await this.$store.dispatch("incomingDocuments/attachCase", {
					id: this.document.id,
					case_id: caseEntity.id,
				});

				this.$emit("attached-case", response);

				if (options.redirect && options.redirect === true) {
					this.$router.push({
						name: "cases.view",
						params: {
							id: caseEntity.id,
						},
					});
				}
			} catch (e) {
				this.$store.dispatch("apiError", {
					error: e,
					title: "Attach Failed",
					message: "An error occurred when attempting to attach to case.",
				});
			} finally {
				if (!redirectAfter) {
					this.$emit("refresh");
				}
			}
		},
	},
};
</script>